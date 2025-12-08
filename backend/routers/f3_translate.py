from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import asyncio
from google.api_core import exceptions as g_api_exceptions

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    target_language: str

@router.post("/feature-3/translate")
async def translate_text(req: TranslateRequest):
    # Prefer newest flash; fall back if quota is exhausted
    model_candidates = [
        "gemini-2.5-flash",
        "models/gemini-1.5-flash",  # v1beta-compatible name
    ]

    prompt = f"""
    Act as a professional translator.
    
    Input Text: "{req.text}"
    Target Language: "{req.target_language}"
    
    Task: Translate the input text accurately into the target language. 
    Maintain the original tone and meaning.
    
    Return JSON with this EXACT format:
    {{
        "translated_text": "Your translated text here"
    }}
    Output ONLY Valid JSON.
    """

    last_error = None

    for model_name in model_candidates:
        model = genai.GenerativeModel(model_name)

        # Try twice per model to gracefully respect short retry windows
        for _ in range(2):
            try:
                response = model.generate_content(prompt)
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(clean_text)
            except g_api_exceptions.ResourceExhausted as e:
                # Respect server suggested retry delay when present
                retry_delay = getattr(e, "retry_delay", None)
                if hasattr(retry_delay, "seconds"):
                    delay_seconds = max(1, min(30, retry_delay.seconds))
                elif isinstance(retry_delay, (int, float)):
                    delay_seconds = max(1, min(30, int(retry_delay)))
                else:
                    delay_seconds = 15
                last_error = e
                await asyncio.sleep(delay_seconds)
                continue
            except Exception as e:  # Keep behavior unchanged for other errors
                last_error = e
                break

    print(f"Error calling Gemini: {last_error}")
    return {
        "translated_text": "Error: Quota exceeded or service unavailable. Please retry in a bit or upgrade your Gemini plan."
    }