CRITICAL_FIELDS = {

    "building_type": {
        "question": "What type of building is it? (Office, Retail, Hospital, Residential, Industrial)",
        "priority": 1
    },

    "area_sqft": {
        "question": "What is the approximate building area in square feet?",
        "priority": 2
    },

    "occupancy": {
        "question": "How many people typically occupy the building?",
        "priority": 3
    },

    "budget_level": {
        "question": "What is the budget level? (Low, Medium, High)",
        "priority": 4
    },

    "floors": {
        "question": "How many floors does the building have?",
        "priority": 5
    }
}


def get_missing_critical_fields(metadata_features):

    missing = []

    for field, config in CRITICAL_FIELDS.items():

        feature = metadata_features.get(field)

        if feature is None:
            continue

        if feature["value"] is None:

            missing.append({
                "field": field,
                "priority": config["priority"],
                "question": config["question"]
            })

    missing = sorted(
        missing,
        key=lambda x: x["priority"]
    )

    return missing


def generate_followup_questions(metadata_features):

    missing_fields = get_missing_critical_fields(metadata_features)

    questions = []

    for item in missing_fields:
        questions.append(item["question"])

    return questions