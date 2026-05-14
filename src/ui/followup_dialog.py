import streamlit as st
from src.utils.type_conversion import convert_feature_type

@st.dialog("Complete Missing Information")

def show_followup_dialog(missing_fields,metadata_features):

    st.markdown(
        "Please complete the missing "
        "critical building information."
    )

    answers = {}

    with st.form("followup_form"):

        for item in missing_fields:
            field = item["field"]
            answers[field] = st.text_input(item["question"])

        submitted = st.form_submit_button("Save Information")

        if submitted:
            for item in missing_fields:
                field = item["field"]
                value = convert_feature_type(field,answers[field])

                metadata_features[field]["value"] = value
                metadata_features[field]["source"] = "user"

            st.session_state["metadata_features"] = metadata_features
            st.success("Information updated successfully!")
            st.rerun()