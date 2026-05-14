import streamlit as st

from src.ui.business_dashboard import render_business_dashboard
from src.recommendation.scoring import get_hvac_scores

def render_analysis_tabs(analysis,prediction,metrics,assumptions):

    tabs = st.tabs([
        "Recommendation",
        "Business Insights",
        "Tradeoffs",
        "Building Features",
        "Assumptions"
    ])


    # TAB 1
    with tabs[0]:

        st.subheader("Why This System Was Recommended")
        text = ""
        for point in analysis["summary"]:
            text += f"• {point}\n\n"

        st.markdown(text)
        st.subheader("Alternative Options")

        alt_text = ""
        for alt in analysis["alternatives"]:
            alt_text += f"• {alt}\n"

        st.success(alt_text)

    # BUSINESS INSIGHTS TAB
    with tabs[1]:

        st.markdown("""
    <div class="content-panel">

    <div class="content-title">
    Operational Benchmark Indicators
    </div>

    </div>
    """, unsafe_allow_html=True)

        scores = get_hvac_scores(prediction["recommended_hvac"])
        score_cols = st.columns(2)
        idx = 0

        for metric, score in scores.items():
            with score_cols[idx % 2]:
                st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title" 
    style="font-size:1.25rem;
    font-weight:600;
    color:#111827;">
    {metric}
    </div>

    <div style="
    font-size:1rem;
    font-weight:500;
    color:#111827;
    margin-top:6px;
    ">
    {score}/100
    </div>

    <div style="
    margin-top:10px;
    ">

    <div style="
    width:100%;
    height:10px;
    background:#E5E7EB;
    border-radius:20px;
    overflow:hidden;
    ">

    <div style="
    width:{score}%;
    height:10px;
    background:#111827;
    border-radius:20px;
    ">
    </div>

    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

            idx += 1

    # TAB 3
    with tabs[2]:
        text = ""
        for point in analysis["tradeoffs"]:
            text += f"• {point}\n\n"

        st.warning(text)

    # TAB 4
    with tabs[3]:
        st.markdown("""
    <div class="content-panel">

    <div class="content-title">
    Extracted Building Parameters
    </div>

    </div>
    """, unsafe_allow_html=True)

        rows = []

        for key, value in prediction["input_features"].items():

            clean_key = (key.replace("_", " ").title())
            clean_value = str(value).split(".")[-1]

            rows.append({
                "Feature": clean_key,
                "Value": clean_value
            })

        st.dataframe(
            rows,
            width='stretch',
            hide_index=True
        )

    # ASSUMPTIONS TAB
    with tabs[4]:
        if len(assumptions) == 0:
            st.markdown("""
    <div class="content-panel">

    <div class="content-title">
    No Active Assumptions
    </div>

    <div class="content-text">
    All critical building parameters
    were provided by the user.
    </div>

    </div>
    """, unsafe_allow_html=True)

        else:
            st.markdown("""
    <div class="content-panel">

    <div class="content-title">
    Estimated Parameters
    </div>

    <div class="content-text">
    These values were inferred from
    building context and can be adjusted.
    </div>

    </div>
    """, unsafe_allow_html=True)

            for item in assumptions:
                feature = item["feature"]
                label = (feature.replace("_", " ").title())

                current = item["value"]
                col1, col2 = st.columns([2, 1])
                with col1:
                    updated = st.text_input(
                        label,
                        value=str(current),
                        key=f"assumption_{feature}"
                    )

                with col2:
                    st.write("")
                    st.write("")
                    if st.button("Update",key=f"btn_{feature}"):

                        state = st.session_state["hvac_state"]
                        state["metadata_features"][feature]["value"] = updated
                        state["metadata_features"][feature]["source"] = ("user_modified")

                        # rebuild flattened features
                        updated_flat = {}

                        for k, v in state["metadata_features"].items():
                            updated_flat[k] = v["value"]

                        state["flattened_features"] = updated_flat

                        # rebuild assumptions
                        new_assumptions = []

                        for k, v in state["metadata_features"].items():
                            
                            if v["source"] in ["inferred","derived"]:

                                new_assumptions.append({
                                    "feature": k,
                                    "value": v["value"],
                                    "source": v["source"]
                                })

                        state["assumptions"] = new_assumptions
                        st.success(f"{label} updated.")

                        st.rerun()