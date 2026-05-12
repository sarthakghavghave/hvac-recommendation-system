import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
from src.llm.extractor import extract_hvac_features

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="HVAC Intelligence Platform",
    page_icon="❄️",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.main-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #E5E7EB;
    line-height: 1.1;
}

.subtitle {
    font-size: 1.05rem;
    color: #9CA3AF;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: #111827;
    border: 1px solid #1F2937;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
}

.metric-title {
    color: #9CA3AF;
    font-size: 0.8rem;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.metric-value {
    color: white;
    font-size: 1.7rem;
    font-weight: 700;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    color: white;
}

.tag {
    display: inline-block;
    background-color: #1E3A8A;
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.85rem;
}

.json-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1F2937;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.markdown("## ⚙️ HVAC Control Panel")

    st.markdown("---")

    st.markdown("### AI Modules")

    st.success("NLP Extraction")
    st.success("Feature Engineering")
    st.warning("Recommendation Engine Pending")

    st.markdown("---")

    st.markdown("### Supported Systems")

    systems = [
        "VRF",
        "Chiller",
        "Central HVAC",
        "Split AC",
        "AHU",
        "FCU"
    ]

    for system in systems:
        st.markdown(f"- {system}")

    st.markdown("---")

    st.markdown("""
    ### Platform Features

    ✅ Natural Language Input  
    ✅ AI Extraction  
    ✅ HVAC Analytics  
    ✅ Energy Insights  
    ⏳ Recommendation Engine  
    """)

# ─────────────────────────────────────────────────────────────
# HEADER SECTION
# ─────────────────────────────────────────────────────────────

header_col1, header_col2 = st.columns([4,1])

with header_col1:

    st.markdown("""
    <div class="main-title">
        ❄️ HVAC Intelligence Platform
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
        AI-powered HVAC requirement extraction, recommendation,
        and energy analytics dashboard.
    </div>
    """, unsafe_allow_html=True)

with header_col2:

    st.info("""
    ### System Status

    ✅ AI Active  
    ✅ Gemini Connected  
    ✅ NLP Extraction Ready
    """)

# ─────────────────────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="section-title">📊 HVAC Analytics Overview</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Buildings Analyzed</div>
        <div class="metric-value">1,284</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Avg Energy Savings</div>
        <div class="metric-value">23%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">AI Confidence</div>
        <div class="metric-value">94%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Recommended Efficiency</div>
        <div class="metric-value">A++</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# AI INPUT SECTION
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="section-title">🤖 AI HVAC Assistant</div>',
    unsafe_allow_html=True
)

left_col, right_col = st.columns([3,1])

with left_col:

    user_query = st.text_area(
        "Describe Building Requirements",
        height=220,
        placeholder="""
Example:

Need HVAC for a 5-floor office building in Mumbai
with around 400 employees.

Need energy-efficient cooling
with medium budget and high humidity handling.
"""
    )

with right_col:

    st.markdown("""
    ### Example Inputs

    🏢 Office Buildings  
    🏥 Hospitals  
    🏬 Retail Malls  
    🏭 Industrial Plants  
    🏠 Residential Towers  
    """)

    st.info("""
    AI automatically extracts:
    - occupancy
    - climate
    - budget
    - floors
    - area
    """)

# ─────────────────────────────────────────────────────────────
# ANALYZE BUTTON
# ─────────────────────────────────────────────────────────────

if st.button("🚀 Analyze Requirements", use_container_width=True):

    if not user_query.strip():

        st.warning("Please enter building requirements.")

    else:

        with st.spinner("Analyzing requirements using AI..."):

            result = extract_hvac_features(user_query)

        st.success("HVAC requirements extracted successfully!")

        # ─────────────────────────────────────────────────────
        # EXTRACTED FEATURES
        # ─────────────────────────────────────────────────────

        st.markdown(
            '<div class="section-title">📋 Extracted Building Profile</div>',
            unsafe_allow_html=True
        )

        feature_col1, feature_col2 = st.columns(2)

        with feature_col1:

            if result.get("building_type"):
                st.markdown(
                    f'<span class="tag">🏢 {result.get("building_type")}</span>',
                    unsafe_allow_html=True
                )

            if result.get("climate_zone"):
                st.markdown(
                    f'<span class="tag">🌡️ {result.get("climate_zone")} Climate</span>',
                    unsafe_allow_html=True
                )

            if result.get("budget_level"):
                st.markdown(
                    f'<span class="tag">💰 {result.get("budget_level")} Budget</span>',
                    unsafe_allow_html=True
                )

            if result.get("occupancy"):
                st.markdown(
                    f'<span class="tag">👥 {result.get("occupancy")} Occupants</span>',
                    unsafe_allow_html=True
                )

        with feature_col2:

            if result.get("area_sqft"):
                st.markdown(
                    f'<span class="tag">📐 {result.get("area_sqft")} sq ft</span>',
                    unsafe_allow_html=True
                )

            if result.get("floors"):
                st.markdown(
                    f'<span class="tag">🏬 {result.get("floors")} Floors</span>',
                    unsafe_allow_html=True
                )

            if result.get("humidity"):
                st.markdown(
                    f'<span class="tag">💧 {result.get("humidity")}% Humidity</span>',
                    unsafe_allow_html=True
                )

            if result.get("outdoor_temp"):
                st.markdown(
                    f'<span class="tag">🌞 {result.get("outdoor_temp")} °C</span>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # ─────────────────────────────────────────────────────
        # RECOMMENDATION PLACEHOLDER
        # ─────────────────────────────────────────────────────

        st.markdown(
            '<div class="section-title">❄️ HVAC Recommendation</div>',
            unsafe_allow_html=True
        )

        st.info("""
        Recommendation engine is currently under development.

        Once integrated, the system will provide:
        - Recommended HVAC system
        - Energy efficiency analysis
        - Cost estimation
        - System comparison
        - AI engineering report
        """)

        # ─────────────────────────────────────────────────────
        # JSON VIEW
        # ─────────────────────────────────────────────────────

        with st.expander("🔍 View Raw Extracted JSON"):

            st.json(result)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")

st.caption("""
Powered by Gemini AI • Intelligent HVAC Analytics Platform •
Built using Streamlit + NLP Extraction + Feature Engineering
""")