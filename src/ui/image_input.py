import streamlit as st

def render_image_upload_section():

    st.markdown("""
<div class="content-panel">

<div class="content-text">
Upload a building layout / floor plan
for automated feature extraction.
</div>

</div>
""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload building image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file,use_container_width=True)

    return uploaded_file


def render_extracted_features(features):

    st.markdown("""
<div class="content-panel">

<div class="content-title">
Extracted Building Parameters
</div>

<div class="content-text">
Review and edit extracted values
before generating recommendation.
</div>

</div>
""", unsafe_allow_html=True)

    updated = {}
    cols = st.columns(2)
    idx = 0

    for key, value in features.items():
        label = key.replace("_", " ").title()

        with cols[idx % 2]:
            updated[key] = st.text_input(label,value=str(value),key=f"img_{key}")
        idx += 1

    return updated