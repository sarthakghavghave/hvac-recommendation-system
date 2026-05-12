from pprint import pprint

from src.llm.extractor import extract_hvac_features


user_input = """
We have a medium-sized office building
in a hot climate with around 300 employees.

The building has 4 floors and operates
for nearly 14 hours daily.

We want energy-efficient cooling
but our budget is moderate.
"""


result = extract_hvac_features(user_input)

pprint(result)