import streamlit as st

SCORE_MAP = {
    "Low": 25,
    "Moderate": 50,
    "Moderate to High": 70,
    "High": 85,
    "Very High": 95,
    "Excellent": 100,
    "Strong": 85,
    "Balanced": 60,
    "Limited": 30,
    "Good": 75
}


def render_business_dashboard(metrics):
    st.subheader("📊 Business Insights")

    cols = st.columns(2)
    idx = 0

    for key, value in metrics.items():
        with cols[idx % 2]:
            st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
{key}
</div>

<div class="metric-value"
style="font-size:1rem;">
{value}
</div>

</div>
""", unsafe_allow_html=True)
            # VISUAL SCORE BAR
            if value in SCORE_MAP:
                st.progress(SCORE_MAP[value] / 100)
        idx += 1