from pprint import pprint

from src.llm.extractor import extract_hvac_features
from src.llm.question_generator import generate_followup_questions

user_input = """
We have a 4-floor office building
with around 300 employees
in a hot climate.
"""

result = extract_hvac_features(user_input)

questions = generate_followup_questions(result)

pprint(result)

print("\nFollow-up Questions:\n")

for q in questions:
    print("-", q)