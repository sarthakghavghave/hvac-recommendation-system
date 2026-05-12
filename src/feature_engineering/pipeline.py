from src.feature_engineering.metadata_wrapper import wrap_features
from src.feature_engineering.complete_features import complete_hvac_features
from src.feature_engineering.flatten_features import flatten_features
from src.feature_engineering.assumptions import get_assumptions

def build_feature_pipeline(parsed_data):

    wrapped = wrap_features(parsed_data)
    completed = complete_hvac_features(wrapped)
    assumptions = get_assumptions(completed)
    flattened = flatten_features(completed)

    return {
        "metadata_features": completed,
        "flattened_features": flattened,
        "assumptions": assumptions
    }