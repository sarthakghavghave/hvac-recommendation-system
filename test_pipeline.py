from pprint import pprint

from src.llm.extractor import extract_hvac_features

from src.feature_engineering.pipeline import build_feature_pipeline
from src.llm.question_generator import generate_followup_questions


user_input = """
We have a 4-floor office building
in a hot climate with around
300 employees.

We want an energy-efficient system.
"""

parsed = extract_hvac_features(user_input)

pipeline = build_feature_pipeline(parsed)

questions = generate_followup_questions(pipeline["metadata_features"])

print("\n==============================")
print("PARSED FEATURES")
print("==============================\n")

pprint(parsed)

print("\n==============================")
print("ASSUMPTIONS")
print("==============================\n")

pprint(pipeline["assumptions"])

print("\n==============================")
print("FLATTENED FEATURES")
print("==============================\n")

pprint(pipeline["flattened_features"])

print("\n==============================")
print("FOLLOW-UP QUESTIONS")
print("==============================\n")

for q in questions:
    print("-", q)