import pickle
import pandas as pd

from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "hvac_rf_model.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

FEATURE_ORDER = [

    "building_type",
    "climate_zone",
    "budget_level",

    "area_sqft",
    "floors",
    "ceiling_height",

    "occupancy",
    "operating_hours",
    "building_age",

    "outdoor_temp",
    "humidity",

    "insulation",
    "glass_ratio"
]


def prepare_prediction_input(features):

    clean = {}

    for feature in FEATURE_ORDER:
        value = features.get(feature)
        # enum handling
        if hasattr(value, "value"):
            value = value.value

        clean[feature] = value

    return pd.DataFrame([clean]), clean


def predict_hvac(features):
    input_df, clean_features = prepare_prediction_input(features)

    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    class_names = model.classes_

    probability_map = []

    for cls, prob in zip(class_names, probabilities):

        probability_map.append({
            "system": cls,
            "confidence": round(prob * 100, 2)
        })

    probability_map = sorted(
        probability_map,
        key=lambda x: x["confidence"],
        reverse=True
    )

    return {
        "recommended_hvac": prediction,
        "confidence": probability_map[0]["confidence"],
        "top_recommendations": probability_map[:3],
        "input_features": clean_features
    }