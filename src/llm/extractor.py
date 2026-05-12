from src.llm.parser import parse_user_input
from src.llm.validator import validate_extracted_json
from src.feature_engineering.derive_features import derive_missing_features

def extract_hvac_features(user_text):

    extracted = parse_user_input(user_text)

    validated = validate_extracted_json(extracted)

    completed = derive_missing_features(validated)

    return completed