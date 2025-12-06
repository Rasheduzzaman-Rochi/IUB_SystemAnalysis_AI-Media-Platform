from fastapi import APIRouter
import google.generativeai as genai
import os

router = APIRouter()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY", "your-key-here")
genai.configure(api_key=api_key)

@router.get("/feature-3")
async def feature_three_test():
    return {"message": "Translation Ready"}

@router.post("/feature-3/translate")
async def translate_text(request: dict):
    try:
        text = request.get("text", "")
        target_language = request.get("target_language", "Bengali")
        
        if not text:
            return {"translated_text": ""}
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Translate the following text to {target_language}. Return ONLY the translated text, nothing else.

Text: {text}"""
        
        response = model.generate_content(prompt)
        return {"translated_text": response.text.strip()}
    except Exception as e:
        print(f"Error: {e}")
        return {"translated_text": f"[Translation to {request.get('target_language', 'Unknown')}]"}