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
from src.llm.question_generator import CRITICAL_FIELDS
from src.models.predict import predict_hvac

from src.recommendation.explainer import generate_recommendation_summary
from src.recommendation.business_metrics import generate_business_metrics
from src.ui.followup_dialog import show_followup_dialog
from src.ui.recommendation_card import render_recommendation_hero
from src.ui.tabs_renderer import render_analysis_tabs

# FILE STORAGE
def get_feature_state_path():
    root_dir = Path(__file__).resolve().parents[1]
    output_dir = root_dir / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / "hvac_feature_state.json"

def save_feature_state(payload, path):

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            indent=2
        )


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
        "pipeline_started": True,
        "user_query": user_query,
        "metadata_features":
            pipeline_result[
                "metadata_features"
            ],

        "flattened_features":
            pipeline_result[
                "flattened_features"
            ],

        "assumptions":
            pipeline_result[
                "assumptions"
            ]
    }
    
    save_feature_state(payload, path)

    st.session_state["hvac_state"] = payload


def initialize_hvac_state(path):

    if "hvac_state" not in st.session_state:

        loaded_state = load_feature_state(path)

        if loaded_state is None:

            st.session_state["hvac_state"] = {

                "user_query": "",
                "metadata_features": {},
                "flattened_features": {},
                "assumptions": [],
                "pipeline_started": False
            }

        else:
            # backward compatibility
            if "pipeline_started" not in loaded_state:

                loaded_state[
                    "pipeline_started"
                ] = False

            st.session_state[
                "hvac_state"
            ] = loaded_state

# MISSING FIELD CHECK
def get_missing_fields(metadata_features):

    missing = []

    for field, config in CRITICAL_FIELDS.items():

        feature = metadata_features.get(field)

        if feature is None:
            continue

        if feature["value"] is None:

            missing.append({
                "field": field,
                "question":
                    config["question"]
            })

    return missing

# INITIALIZE
FEATURE_STATE_PATH = (
    get_feature_state_path()
)

initialize_hvac_state(
    FEATURE_STATE_PATH
)

# PAGE CONFIG
st.set_page_config(
    page_title="\nHVAC Intelligence Platform",
    layout="wide",
    page_icon="❄️"
)

# STYLES
st.markdown("""
<style>
/* GLOBAL */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F3F4F6;
    color: #111827;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADER */
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.25rem;
}

.subtitle {
    font-size: 1rem;
    color: #6B7280;
    margin-bottom: 2rem;
}

/* INPUT */
textarea {
    border-radius: 14px !important;
    border: 1px solid #D1D5DB !important;
    background-color: white !important;
    color: #111827 !important;
    font-size: 15px !important;
}

/* BUTTON */
.stButton > button {
    background-color: #1F2937;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.65rem 1rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {

    background-color: #111827;
}

/* CARDS */
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    margin-bottom: 16px;
    box-shadow:
        0 1px 3px rgba(0,0,0,0.04);
}

.metric-title {
    color: #6B7280;
    font-size: 0.8rem;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.metric-value {
    color: #111827;
    font-size: 1.35rem;
    font-weight: 700;
}

.hero-card {
    background-color: white;
    border: 1px solid #D1D5DB;
    border-left: 6px solid #111827;
    border-radius: 18px;
    padding: 28px;
    margin-top: 10px;
    margin-bottom: 24px;
    box-shadow:
        0 4px 10px rgba(0,0,0,0.05);
}

.hero-label {
    color: #6B7280;
    font-size: 0.9rem;
    text-transform: uppercase;
    margin-bottom: 12px;
    letter-spacing: 0.04em;
}

.hero-system {
    font-size: 2.3rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 12px;
}

.hero-confidence {
    color: #4B5563;
    font-size: 1rem;
    font-weight: 500;
}
            
.hero-description {
    color: #374151;
    font-size: 1rem;
    margin-bottom: 14px;
    line-height: 1.6;
}
            
/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 10px;
    padding: 10px 18px;
    border: 1px solid #E5E7EB;
    color: #374151;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #111827 !important;
    color: white !important;
}

/* ALERTS */
.stAlert {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    """
<div class="main-title">
❄️ HVAC Intelligence Platform
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
AI-assisted HVAC recommendation platform
for commercial building decision support.
</div>
""",
    unsafe_allow_html=True
)

# INPUT MODE
st.subheader(
    "🏢 Building Input"
)

input_mode = st.radio(

    "Choose input method",

    [
        "Text Description",
        "Upload Image"
    ],

    horizontal=True
)

# TEXT INPUT
if input_mode == "Text Description":

    user_query = st.text_area(

        "Describe the building and HVAC requirements",

        height=220,

        value=st.session_state[
            "hvac_state"
        ]["user_query"],

        placeholder="""Example:
We are planning HVAC for a 6-floor corporate office in a hot climate with nearly 1200 employees.
Energy efficiency is important and the budget is high.
""",

        key="user_query"
    )

# IMAGE INPUT
else:

    from src.ui.image_input import (
        render_image_upload_section,
        render_extracted_features
    )

    uploaded_file = (
        render_image_upload_section()
    )

    if uploaded_file is not None:

        extract_clicked = st.button(

            "Extract Building Features",

            use_container_width=True
        )

        if extract_clicked:

            with st.spinner(
                "Extracting building parameters..."
            ):

                # TEMPORARY MOCK RESPONSE
                extracted_json = {
                    "building_type": "Office",
                    "floors": 4,
                    "area_sqft": 18000,
                    "occupancy": 350,
                    "ceiling_height": 11,
                    "climate_zone": "Humid"
                }

                st.session_state[
                    "image_features"
                ] = extracted_json

        if "image_features" in st.session_state:

            edited = render_extracted_features(

                st.session_state[
                    "image_features"
                ]
            )

            generate_clicked = st.button(

                "Generate Recommendation",

                use_container_width=True
            )

            if generate_clicked:

                st.success(
                    "Image feature pipeline ready for integration."
                )

                st.json(edited)

# BUTTON
analyze_clicked = st.button(
    "Generate Recommendation",
    use_container_width=True
)

if analyze_clicked:

    if not st.session_state[
        "user_query"
    ].strip():

        st.warning(
            "Please enter building details."
        )

    else:

        try:

            with st.spinner(
                "Analyzing requirements..."
            ):

                parsed_data = (
                    extract_hvac_features(
                        st.session_state[
                            "user_query"
                        ]
                    )
                )

                pipeline_result = (
                    build_feature_pipeline(
                        parsed_data
                    )
                )

                persist_pipeline_result(

                    pipeline_result,

                    st.session_state[
                        "user_query"
                    ],

                    FEATURE_STATE_PATH
                )

            st.success(
                "Recommendation generated successfully."
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# MAIN FLOW
metadata_features = st.session_state[
    "hvac_state"
]["metadata_features"]

assumptions = st.session_state[
    "hvac_state"
]["assumptions"]

flattened_features = st.session_state[
    "hvac_state"
]["flattened_features"]

if metadata_features and st.session_state["hvac_state"]["pipeline_started"]:

    # FOLLOW-UP QUESTIONS
    missing_fields = get_missing_fields(
        metadata_features
    )

    if len(missing_fields) > 0:

        show_followup_dialog(

            missing_fields,
            metadata_features
        )

        st.warning( 
            "Complete missing building information."
        )

    else:

        try:

            # PREDICTION
            prediction = predict_hvac(
                flattened_features
            )

            recommended = prediction[
                "recommended_hvac"
            ]

            # HERO SECTION
            st.markdown("---")

            render_recommendation_hero(
                prediction
            )

            # ANALYSIS
            analysis = (
                generate_recommendation_summary(
                    recommended,
                    flattened_features,
                    prediction[
                        "top_recommendations"
                    ]
                )
            )

            metrics = (
                generate_business_metrics(
                    recommended,
                    flattened_features
                )
            )

            # TABS
            st.markdown("---")
            render_analysis_tabs(
                analysis,
                prediction,
                metrics,
                assumptions
            )

        except Exception as e:
            st.error(
                f"Prediction Error: {str(e)}"
            )

# FOOTER
st.markdown("---")

st.caption("""
HVAC Intelligence Platform •
AI-assisted commercial HVAC recommendation workflow
""")