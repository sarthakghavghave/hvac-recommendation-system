import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st

from src.llm.extractor import extract_hvac_features
from src.feature_engineering.pipeline import build_feature_pipeline
from src.llm.question_generator import generate_followup_questions

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="HVAC Intelligence Platform",
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
    placeholder="""
Example:

Need HVAC for a 5-floor office building in Mumbai
with around 400 employees.

Need energy-efficient cooling
with medium budget and high humidity handling.
"""
)

# ─────────────────────────────────────────────────────────────
# ANALYZE
# ─────────────────────────────────────────────────────────────

if st.button("🚀 Analyze Requirements", use_container_width=True):

    if not user_query.strip():

        st.warning("Please enter building requirements.")

    else:

        try:

            with st.spinner("Analyzing requirements using AI..."):

                parsed_data = extract_hvac_features(user_query)

                pipeline_result = build_feature_pipeline(
                    parsed_data
                )

                metadata_features = pipeline_result[
                    "metadata_features"
                ]

                flattened_features = pipeline_result[
                    "flattened_features"
                ]

                assumptions = pipeline_result[
                    "assumptions"
                ]

                questions = generate_followup_questions(
                    metadata_features
                )

            st.success(
                "HVAC analysis completed successfully!"
            )

            st.markdown("---")

            # ─────────────────────────────────────────────
            # FEATURES
            # ─────────────────────────────────────────────

            st.subheader("📊 Features")

            feature_items = []

            for feature, info in metadata_features.items():

                if info["value"] is not None:

                    feature_items.append(
                        (
                            feature,
                            info["value"]
                        )
                    )

            cols = st.columns(4)

            for idx, (feature, value) in enumerate(
                feature_items
            ):

                clean_name = (
                    feature
                    .replace("_", " ")
                    .title()
                )

                clean_value = str(value).split(".")[-1]

                with cols[idx % 4]:

                    st.markdown(f"""
<div class="metric-card">
<div class="metric-title">{clean_name}</div>
<div class="metric-value">{clean_value}</div>
</div>
""", unsafe_allow_html=True)

            # ─────────────────────────────────────────────
            # ASSUMPTIONS
            # ─────────────────────────────────────────────

            if assumptions:

                st.markdown("---")

                st.subheader(
                    "🧠 Assumed / Derived Features"
                )

                assumption_cols = st.columns(3)

                for idx, item in enumerate(assumptions):

                    feature_name = item["feature"]

                    feature_value = item["value"]

                    feature_source = item["source"]

                    clean_name = (
                        feature_name
                        .replace("_", " ")
                        .title()
                    )

                    clean_value = str(
                        feature_value
                    ).split(".")[-1]

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

                        if st.button(
                            f"Save {clean_name}",
                            key=f"save_{feature_name}"
                        ):

                            metadata_features[
                                feature_name
                            ]["value"] = updated_value

                            metadata_features[
                                feature_name
                            ]["source"] = "user_modified"

                            st.success(
                                f"{clean_name} updated."
                            )

            # ─────────────────────────────────────────────
            # FOLLOW-UP QUESTIONS
            # ─────────────────────────────────────────────

            if questions:

                st.markdown("---")

                st.subheader(
                    "❓ Missing Information"
                )

                for question in questions:

                    st.markdown(f"""
<div class="question-box">
{question}
</div>
""", unsafe_allow_html=True)

                    st.text_input(
                        label="",
                        placeholder="Enter response here...",
                        key=f"question_{question}"
                    )

            # ─────────────────────────────────────────────
            # RECOMMENDATION PLACEHOLDER
            # ─────────────────────────────────────────────

            st.markdown("---")

            st.subheader(
                "❄️ HVAC Recommendation"
            )

            st.info("""
Recommendation engine integration pending.

Future output will include:
- Recommended HVAC system
- Energy efficiency analysis
- Cost estimation
- System comparison
""")

            # ─────────────────────────────────────────────
            # RAW OUTPUT
            # ─────────────────────────────────────────────

            with st.expander(
                "🔍 View Raw Pipeline Output"
            ):

                st.json(pipeline_result)

        except Exception as e:

            st.error(f"Error: {str(e)}")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")

st.caption("""
HVAC AI Platform • Streamlit • Gemini AI •
NLP Extraction • Feature Engineering • Intelligent HVAC Analysis
""")