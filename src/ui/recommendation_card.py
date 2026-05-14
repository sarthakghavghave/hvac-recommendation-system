import streamlit as st


SYSTEM_DESCRIPTIONS = {

    "VRF":
        "Recommended for multi-zone commercial buildings prioritizing energy-efficient climate control.",

    "Multi-Split":
        "Suitable for medium-sized commercial buildings with flexible room-level cooling requirements.",

    "Central Chiller":
        "Designed for large-scale centralized cooling with continuous operational demand.",

    "Split AC":
        "Best suited for compact buildings with localized cooling needs and lower infrastructure complexity.",

    "Packaged Unit":
        "Appropriate for commercial spaces requiring simplified centralized HVAC deployment."
}


def render_recommendation_hero(prediction):

    system = prediction["recommended_hvac"]
    confidence = prediction["confidence"]
    subtitle = SYSTEM_DESCRIPTIONS.get(
        system,
        "Commercial HVAC recommendation generated."
    )

    st.markdown(f"""
<div class="hero-card">

<div class="hero-label">
Recommended HVAC System
</div>

<div class="hero-system">
{system}
</div>

<div class="hero-description">
{subtitle}
</div>

<div class="hero-confidence">
Model Confidence: {confidence}%
</div>

</div>
""", unsafe_allow_html=True)