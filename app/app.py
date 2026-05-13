import sys
import os
import json
from pathlib import Path

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st

from src.llm.extractor import extract_hvac_features
from src.feature_engineering.pipeline import build_feature_pipeline
from src.llm.question_generator import CRITICAL_FIELDS, generate_followup_questions


def get_feature_state_path():
    root_dir = Path(__file__).resolve().parents[1]
    output_dir = root_dir / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / "hvac_feature_state.json"


def save_feature_state(payload, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def load_feature_state(path):
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return None


def persist_pipeline_result(pipeline_result, user_query, path):
    payload = {
        "user_query": user_query,
        "metadata_features": pipeline_result["metadata_features"],
        "flattened_features": pipeline_result["flattened_features"],
        "assumptions": pipeline_result["assumptions"]
    }
    save_feature_state(payload, path)
    st.session_state["hvac_state"] = payload


def rebuild_pipeline_from_metadata(metadata_features):
    flattened = {key: info["value"] for key, info in metadata_features.items()}
    return build_feature_pipeline(flattened)


def initialize_hvac_state(path):
    if "hvac_state" not in st.session_state:
        loaded_state = load_feature_state(path)

        if loaded_state is None:
            st.session_state["hvac_state"] = {
                "user_query": "",
                "metadata_features": {},
                "flattened_features": {},
                "assumptions": []
            }
        else:
            st.session_state["hvac_state"] = loaded_state


FEATURE_STATE_PATH = get_feature_state_path()
initialize_hvac_state(FEATURE_STATE_PATH)

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI-powered HVAC Decision Support for Sales",
    layout="wide",
    page_icon="❄️"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #00BFFF;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.05rem;
    color: #AAAAAA;
    margin-bottom: 1.5rem;
}

.metric-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border-left: 4px solid #00BFFF;
    margin-bottom: 15px;
}

.metric-title {
    font-size: 0.85rem;
    color: #9CA3AF;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 1.35rem;
    font-weight: bold;
    color: white;
    word-wrap: break-word;
}

.question-box {
    background-color: #111827;
    padding: 16px;
    border-radius: 12px;
    border-left: 4px solid #EF4444;
    margin-bottom: 12px;
    color: white;
}

.assumption-card {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border-left: 4px solid #F59E0B;
    margin-bottom: 15px;
}

.assumption-label {
    color: #9CA3AF;
    font-size: 0.85rem;
    text-transform: uppercase;
}

.assumption-value {
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 10px;
}

.assumption-source {
    color: #AAAAAA;
    font-size: 0.8rem;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="main-title">❄️ HVAC Intelligence Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered HVAC extraction and intelligent building analysis dashboard.</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.header("⚙️ HVAC Platform")

    st.markdown("---")

    st.success("NLP Extraction")
    st.success("Feature Pipeline")
    st.warning("Recommendation Engine Pending")

    st.markdown("---")

    st.write("### Supported Systems")

    st.write("""
- VRF
- Chiller
- Split AC
- AHU
- FCU
""")

# ─────────────────────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────────────────────

st.subheader("📝 Describe Building Requirements")

user_query = st.text_area(
    "Enter natural language HVAC requirements",
    height=220,
    value=st.session_state["hvac_state"]["user_query"],
    placeholder="""
Example:

Need HVAC for a 5-floor office building in Mumbai
with around 400 employees.

Need energy-efficient cooling
with medium budget and high humidity handling.
""",
    key="user_query"
)


def get_missing_fields(metadata_features):
    missing = []

    for field, config in CRITICAL_FIELDS.items():
        feature = metadata_features.get(field)

        if feature is None:
            continue

        if feature["value"] is None:
            missing.append({
                "field": field,
                "question": config["question"]
            })

    return missing


def render_feature_dashboard(metadata_features, assumptions):
    st.markdown("---")
    st.subheader("📊 Features")

    feature_items = []
    for feature, info in metadata_features.items():
        if info["value"] is not None:
            feature_items.append((feature, info["value"]))

    cols = st.columns(4)
    for idx, (feature, value) in enumerate(feature_items):
        clean_name = feature.replace("_", " ").title()
        clean_value = str(value).split(".")[-1]

        with cols[idx % 4]:
            st.markdown(f"""
<div class="metric-card">
<div class="metric-title">{clean_name}</div>
<div class="metric-value">{clean_value}</div>
</div>
""", unsafe_allow_html=True)

    if assumptions:
        st.markdown("---")
        st.subheader("🧠 Assumed / Derived Features")
        assumption_cols = st.columns(3)

        for idx, item in enumerate(assumptions):
            feature_name = item["feature"]
            feature_value = item["value"]
            feature_source = item["source"]
            clean_name = feature_name.replace("_", " ").title()
            clean_value = str(feature_value).split(".")[-1]

            with assumption_cols[idx % 3]:
                st.markdown(f"""
<div class="assumption-card">
<div class="assumption-label">
{clean_name}
</div>

<div class="assumption-value">
{clean_value}
</div>

<div class="assumption-source">
Source: {feature_source}
</div>
</div>
""", unsafe_allow_html=True)

                updated_value = st.text_input(
                    f"Modify {clean_name}",
                    value=str(clean_value),
                    key=f"update_{feature_name}"
                )

                if st.button(f"Save {clean_name}", key=f"save_{feature_name}"):
                    metadata_features[feature_name]["value"] = updated_value
                    metadata_features[feature_name]["source"] = "user_modified"
                    pipeline_result = rebuild_pipeline_from_metadata(metadata_features)
                    persist_pipeline_result(pipeline_result, st.session_state["user_query"], FEATURE_STATE_PATH)
                    st.success(f"{clean_name} updated.")


def build_raw_output_summary(metadata_features, flattened_features, assumptions):
    summary = []

    for feature, info in metadata_features.items():
        summary.append({
            "Feature": feature.replace("_", " ").title(),
            "Value": info["value"],
            "Source": info["source"]
        })

    return {
        "summary": summary,
        "flattened_features": flattened_features,
        "assumptions": [
            {
                "Feature": item["feature"].replace("_", " ").title(),
                "Value": item["value"],
                "Source": item["source"]
            }
            for item in assumptions
        ]
    }

# ─────────────────────────────────────────────────────────────
# ANALYZE
# ─────────────────────────────────────────────────────────────

analyze_clicked = st.button("🚀 Analyze Requirements", use_container_width=True)

if analyze_clicked:
    if not st.session_state["user_query"].strip():
        st.warning("Please enter building requirements.")
    else:
        try:
            with st.spinner("Analyzing requirements using AI..."):
                parsed_data = extract_hvac_features(st.session_state["user_query"])
                pipeline_result = build_feature_pipeline(parsed_data)
                persist_pipeline_result(pipeline_result, st.session_state["user_query"], FEATURE_STATE_PATH)

            st.success("HVAC analysis completed successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

metadata_features = st.session_state["hvac_state"]["metadata_features"]
assumptions = st.session_state["hvac_state"]["assumptions"]
questions = generate_followup_questions(metadata_features)

if metadata_features:
    render_feature_dashboard(metadata_features, assumptions)

    missing_fields = get_missing_fields(metadata_features)
    if missing_fields:
        st.markdown("---")
        st.subheader("❓ Missing Information")

        with st.form("missing_answers_form"):
            for item in missing_fields:
                st.text_input(
                    item["question"],
                    key=f"missing_{item['field']}",
                    value=st.session_state.get(f"missing_{item['field']}", "")
                )

            if st.form_submit_button("Save Missing Information"):
                updated = False
                for item in missing_fields:
                    answer = st.session_state.get(f"missing_{item['field']}", "").strip()
                    if answer:
                        metadata_features[item["field"]]["value"] = answer
                        metadata_features[item["field"]]["source"] = "user"
                        updated = True

                if updated:
                    pipeline_result = rebuild_pipeline_from_metadata(metadata_features)
                    persist_pipeline_result(pipeline_result, st.session_state["user_query"], FEATURE_STATE_PATH)
                    st.success("Missing information saved and pipeline refreshed.")
                else:
                    st.info("No new answers were provided.")

    st.markdown("---")
    st.subheader("❄️ HVAC Recommendation")
    st.info('''
Recommendation engine integration pending.

Future output will include:
- Recommended HVAC system
- Energy efficiency analysis
- Cost & ROI estimation
- System comparison
''')

    with st.expander("🔍 View Raw Pipeline Output"):
        raw_output = build_raw_output_summary(
            metadata_features,
            st.session_state["hvac_state"]["flattened_features"],
            assumptions
        )

        st.write("### Feature summary")
        st.table(raw_output["summary"])

        st.write("### Flattened features")
        st.json(raw_output["flattened_features"])

        if raw_output["assumptions"]:
            st.write("### Assumptions")
            st.table(raw_output["assumptions"])

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")

st.caption("""
HVAC AI Platform • Streamlit • Gemini AI •
NLP Extraction • Feature Engineering • Intelligent HVAC Analysis
""")