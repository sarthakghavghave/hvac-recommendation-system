# ─────────────────────────────────────────────────────────────────────
# floor_extractor.py
# Extracts ONLY: area_sqft, floors, glass_ratio
# ─────────────────────────────────────────────────────────────────────

import cv2
import numpy as np
import json
import re
import io
import os
import time
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai

# ─────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────
GLASS_RATIO_MAP = {
    "Low":    0.2,
    "Medium": 0.4,
    "High":   0.6
}


# ─────────────────────────────────────────────────────────────────────
# Configure Gemini
# ─────────────────────────────────────────────────────────────────────
def configure_gemini():
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not set. "
            "Add it to your environment variables."
        )
    genai.configure(api_key=api_key)


# ═════════════════════════════════════════════════════════════════════
# PHASE 1 — UPLOAD & VALIDATE
# ═════════════════════════════════════════════════════════════════════

def load_image(uploaded_file) -> np.ndarray:
    """
    Read and validate Streamlit UploadedFile.
    Returns rgb_array (H×W×3 uint8).
    """
    uploaded_file.seek(0)
    raw = uploaded_file.read()

    try:
        img = Image.open(io.BytesIO(raw))
        img.verify()
        img = Image.open(io.BytesIO(raw))
    except UnidentifiedImageError:
        raise ValueError(
            "Not a recognised image format. "
            "Please upload PNG, JPG, or WEBP."
        )
    except Exception as e:
        raise ValueError(f"Corrupt or unreadable file: {e}")

    w, h = img.size
    if w < 200 or h < 200:
        raise ValueError(
            f"Image too small ({w}×{h}px). "
            "Minimum 200×200px required."
        )

    rgb_array = np.array(img.convert("RGB"))
    print(f"[Phase 1] Loaded: {w}×{h}px")
    return rgb_array


# ═════════════════════════════════════════════════════════════════════
# PHASE 2 — OPENCV PREPROCESSING
# ═════════════════════════════════════════════════════════════════════

def preprocess(rgb_array: np.ndarray) -> np.ndarray:
    """
    Converts image to binary wall map.
    Returns 'closed' binary array — fed into Phase 3.
    """
    gray    = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh  = cv2.adaptiveThreshold(
                  blurred, 255,
                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                  cv2.THRESH_BINARY_INV,
                  15, 2
              )
    kernel  = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed  = cv2.morphologyEx(
                  thresh, cv2.MORPH_CLOSE, kernel, iterations=2
              )

    print(f"[Phase 2] Preprocessing done")
    return closed


# ═════════════════════════════════════════════════════════════════════
# PHASE 3 — AREA MEASUREMENT
# Extracts: area_sqft
# ═════════════════════════════════════════════════════════════════════

def measure_area(closed: np.ndarray,
                 known_area_m2: float = None) -> tuple:
    """
    Detects room contours and sums total floor area.

    Extracts: area_sqft — the only Phase 3 dataset feature.
    Returns:  (total_area_sqft, rooms, rooms_raw)
              rooms and rooms_raw kept for Phase 4 annotation only.
    """
    contours, hierarchy = cv2.findContours(
        closed,
        cv2.RETR_CCOMP,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if hierarchy is None:
        raise ValueError("No contours found in image.")

    h         = hierarchy[0]
    rooms_raw = []
    envelope  = None

    for i, cnt in enumerate(contours):
        area   = cv2.contourArea(cnt)
        parent = h[i][3]

        if area < 500:
            continue

        if parent == -1:
            if envelope is None or area > cv2.contourArea(envelope):
                envelope = cnt
        else:
            rooms_raw.append({
                "contour": cnt,
                "area_px": area
            })

    if not rooms_raw:
        raise ValueError(
            "No rooms detected. Try a clearer image "
            "or use Manual Entry mode."
        )

    # Scale calibration px² → m²
    total_px2 = sum(r["area_px"] for r in rooms_raw)
    if known_area_m2 and known_area_m2 > 0 and total_px2 > 0:
        scale_factor = known_area_m2 / total_px2
        print(f"[Phase 3] Scale: user-provided")
    else:
        scale_factor = 0.01
        print(f"[Phase 3] Scale: estimated")

    # Build room list with centroids (needed for annotation only)
    rooms = []
    for i, r in enumerate(sorted(
        rooms_raw, key=lambda x: x["area_px"], reverse=True
    )):
        cnt       = r["contour"]
        area_m2   = round(r["area_px"] * scale_factor, 2)
        area_sqft = round(area_m2 * 10.764, 1)

        x, y, w, h2 = cv2.boundingRect(cnt)
        M  = cv2.moments(cnt)
        cx = int(M["m10"] / M["m00"]) if M["m00"] != 0 else x + w // 2
        cy = int(M["m01"] / M["m00"]) if M["m00"] != 0 else y + h2 // 2

        rooms.append({
            "room_id":   i + 1,
            "contour":   cnt,
            "area_m2":   area_m2,
            "area_sqft": area_sqft,
            "centroid":  {"x": cx, "y": cy}
        })

    # ── The one dataset feature from Phase 3 ─────────────────────────
    total_area_sqft = round(sum(r["area_sqft"] for r in rooms), 1)
    total_area_m2   = round(sum(r["area_m2"]   for r in rooms), 2)

    print(f"[Phase 3] area_sqft = {total_area_sqft} "
          f"({total_area_m2} m²) | {len(rooms)} rooms detected")

    return total_area_sqft, total_area_m2, rooms


# ═════════════════════════════════════════════════════════════════════
# PHASE 4 — GEMINI VISION
# Extracts: glass_ratio
# ═════════════════════════════════════════════════════════════════════

def annotate_image(rgb_array: np.ndarray,
                   rooms: list) -> np.ndarray:
    """
    Stamps area labels on rooms before sending to Gemini.
    Gemini's job is then glazing estimation only — not area.
    """
    annotated = rgb_array.copy()

    for room in rooms:
        cnt = room["contour"]
        cx  = room["centroid"]["x"]
        cy  = room["centroid"]["y"]

        cv2.drawContours(annotated, [cnt], -1, (0, 200, 80), 2)

        for j, label in enumerate([
            f"R{room['room_id']}: {room['area_m2']}m2",
            f"({room['area_sqft']} sqft)"
        ]):
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1
            )
            lx = cx - tw // 2
            ly = cy + j * 18
            cv2.rectangle(annotated,
                          (lx-3, ly-th-2), (lx+tw+3, ly+3),
                          (0, 0, 0), -1)
            cv2.putText(annotated, label, (lx, ly),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42,
                        (0, 255, 100), 1, cv2.LINE_AA)

    return annotated


def call_gemini_vision(pil_img: Image.Image,
                        building_type: str,
                        total_area_m2: float,
                        floor_count: int) -> str:
    """
    Sends annotated floor plan to Gemini.
    Asks ONLY for glazing level — the one thing Gemini
    provides that maps to a dataset feature (glass_ratio).
    Room zone classification removed — not a dataset feature.
    """
    model = genai.GenerativeModel(
        model_name        = "gemini-2.0-flash-lite",
        generation_config = {
            "temperature":       0.1,
            "top_p":             0.9,
            "max_output_tokens": 200,   # small — only need glazing
        }
    )

    prompt = f"""You are an HVAC engineer analyzing a floor plan image.

Building: {building_type}, {total_area_m2} m2, {floor_count} floor(s).

Look at the floor plan and estimate the glazing level —
how much of the walls are covered by windows.

Return ONLY valid JSON. No markdown. No explanation.
Start with {{ and end with }}.

{{
  "glazing"   : "<Low|Medium|High>",
  "confidence": <integer 0 to 100>
}}

Glazing guide:
- Low    = very few or small windows (< 20% of wall area)
- Medium = normal window coverage (20-40% of wall area)
- High   = large or many windows, glass walls (> 40% of wall area)

Never use null. Return exactly these 2 fields."""

    print("[Phase 4] Calling Gemini for glazing estimation...")
    response = model.generate_content([pil_img, prompt])
    raw      = response.text.strip()
    print(f"[Phase 4] Response: {raw}")
    return raw


def parse_glazing_response(raw_text: str) -> tuple:
    """
    Parse Gemini's glazing JSON response.
    Returns (glass_ratio float, confidence int).
    """
    clean = re.sub(r"```json|```", "", raw_text).strip()
    match = re.search(r"\{[\s\S]*\}", clean)

    if not match:
        print("[Phase 4] Warning: could not parse response, "
              "defaulting to Medium glazing")
        return 0.4, 0

    parsed = json.loads(match.group(0))

    glazing    = parsed.get("glazing", "Medium")
    confidence = parsed.get("confidence", 0)

    # Validate glazing value
    if glazing not in GLASS_RATIO_MAP:
        print(f"[Phase 4] Warning: unknown glazing '{glazing}', "
              "defaulting to Medium")
        glazing = "Medium"

    glass_ratio = GLASS_RATIO_MAP[glazing]

    print(f"[Phase 4] glass_ratio = {glass_ratio} "
          f"(glazing: {glazing} | confidence: {confidence}%)")

    return glass_ratio, glazing, confidence


def get_glass_ratio_with_retry(pil_img: Image.Image,
                                building_type: str,
                                total_area_m2: float,
                                floor_count: int,
                                max_retries: int = 3) -> tuple:
    """
    Calls Gemini with retry + rate limit handling.
    Returns (glass_ratio, glazing, confidence).
    Falls back to 0.4 (Medium) if all retries fail.
    """
    last_error = None
    wait_secs  = 65

    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n[Phase 4] Attempt {attempt}/{max_retries}")
            raw    = call_gemini_vision(
                         pil_img, building_type,
                         total_area_m2, floor_count
                     )
            result = parse_glazing_response(raw)
            print(f"[Phase 4] Success on attempt {attempt}")
            return result

        except Exception as e:
            last_error = e
            err_str    = str(e)

            if "429" in err_str or "TooManyRequests" in err_str:
                match = re.search(r"retry in ([\d.]+)s", err_str)
                wait  = float(match.group(1)) + 5 if match else wait_secs
                print(f"[Phase 4] Rate limited — waiting {wait:.0f}s...")
                time.sleep(wait)
                wait_secs *= 2
            else:
                print(f"[Phase 4] Attempt {attempt} failed: {e}")

    # All retries failed — use safe default
    print(f"[Phase 4] All retries failed ({last_error}). "
          "Defaulting to Medium glazing (glass_ratio=0.4)")
    return 0.4, "Medium", 0


# ═════════════════════════════════════════════════════════════════════
# MASTER FUNCTION — called by app.py
# ═════════════════════════════════════════════════════════════════════

def extract_from_floor_plan(uploaded_file,
                             building_type: str = "Residential",
                             floor_count:   int   = 1,
                             known_area_m2: float = None) -> dict:
    """
    Runs all 4 phases and returns exactly 3 dataset features:

        area_sqft   → measured by OpenCV          (Phase 3)
        floors      → provided by user             (upload form)
        glass_ratio → estimated by Gemini Vision   (Phase 4)

    All other dataset features (building_type, climate_zone,
    budget_level, ceiling_height, occupancy, operating_hours,
    building_age, outdoor_temp, humidity, insulation) must be
    collected from the sidebar in app.py.

    app.py usage:
        extracted     = extract_from_floor_plan(uploaded, ...)
        full_features = {**sidebar_inputs, **extracted}
        result        = predict(full_features, models)
    """
    configure_gemini()

    # ── Phase 1: Load & validate ──────────────────────────────────────
    print("\n" + "="*50)
    print("PHASE 1 — Load & validate")
    print("="*50)
    rgb_array = load_image(uploaded_file)

    # ── Phase 2: OpenCV preprocessing ────────────────────────────────
    print("\n" + "="*50)
    print("PHASE 2 — OpenCV preprocessing")
    print("="*50)
    closed = preprocess(rgb_array)

    # ── Phase 3: Measure area ─────────────────────────────────────────
    print("\n" + "="*50)
    print("PHASE 3 — Area measurement  →  area_sqft")
    print("="*50)
    total_area_sqft, total_area_m2, rooms = measure_area(
        closed,
        known_area_m2 = known_area_m2
    )

    # ── Phase 4: Gemini glazing estimation ────────────────────────────
    print("\n" + "="*50)
    print("PHASE 4 — Gemini Vision  →  glass_ratio")
    print("="*50)
    annotated = annotate_image(rgb_array, rooms)

    pil_img = Image.fromarray(annotated)
    w, h    = pil_img.size
    if max(w, h) > 2048:
        s       = 2048 / max(w, h)
        pil_img = pil_img.resize((int(w*s), int(h*s)), Image.LANCZOS)

    glass_ratio, glazing, confidence = get_glass_ratio_with_retry(
        pil_img,
        building_type = building_type,
        total_area_m2 = total_area_m2,
        floor_count   = floor_count
    )

    # ── Summary ───────────────────────────────────────────────────────
    print("\n" + "="*50)
    print("EXTRACTION COMPLETE")
    print("="*50)
    print(f"  area_sqft  : {total_area_sqft}")
    print(f"  floors     : {floor_count}")
    print(f"  glass_ratio: {glass_ratio}  (glazing: {glazing})")
    print(f"  confidence : {confidence}%")
    print("="*50)

    return {
        # ── 3 dataset features ────────────────────────────────────────
        "area_sqft":   total_area_sqft,
        "floors":      floor_count,
        "glass_ratio": glass_ratio,

        # ── Display only (not passed to ML model) ─────────────────────
        "total_area_m2":   total_area_m2,
        "glazing":         glazing,
        "confidence":      confidence,
        "room_count":      len(rooms),
        "annotated_image": annotated,
        "source":          "floor_plan",
        "extracted_at":    datetime.now().isoformat()
    }