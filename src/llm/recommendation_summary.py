import os

from dotenv import load_dotenv
from google import genai
from src.llm.prompts import SUMMARY_PROMPT

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_llm_summary(recommendation,features,alternatives):
    prompt = f"""
Recommended HVAC System:
{recommendation}

Building Features:
{features}

Alternative Systems:
{alternatives}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[SUMMARY_PROMPT,prompt]
        )

        text = response.text

        sections = {
            "recommendation": "",
            "fit": "",
            "tradeoff": ""
        }

        current = None

        for line in text.splitlines():
            line = line.strip()
            if "[EXECUTIVE_RECOMMENDATION]" in line:
                current = "recommendation"
                continue

            elif "[WHY_IT_FITS]" in line:
                current = "fit"
                continue

            elif "[TRADEOFF]" in line:
                current = "tradeoff"
                continue

            if current and line:
                sections[current] += line + "\n"

        return sections

    except Exception as e:

        return {
            "recommendation":
                "AI executive briefing is currently unavailable.",

            "fit":
                "- Recommendation analysis could not be generated.\n"
                "- Core HVAC prediction remains available.",

            "tradeoff":
                "Please retry summary generation."
        }