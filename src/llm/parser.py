import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.llm.prompts import EXTRACTION_PROMPT
from src.llm.schema import HVACInputSchema

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def parse_user_input(user_text):

    prompt = f"""
    {EXTRACTION_PROMPT}

    User Input:
    {user_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=HVACInputSchema
            )
        )

        if response.parsed:
            # response.parsed is an instance of HVACInputSchema
            return response.parsed.model_dump()
        else:
            return {
                "error": "Model returned empty parsed response",
                "raw": response.text
            }

    except Exception as e:
        return {
            "error": f"Failed to parse response: {str(e)}"
        }