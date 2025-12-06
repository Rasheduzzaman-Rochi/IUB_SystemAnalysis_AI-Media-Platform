from fastapi import APIRouter
import google.generativeai as genai
import os

router = APIRouter()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY", "your-key-here")
genai.configure(api_key=api_key)

@router.get("/feature-1")
async def feature_one_test():
    return {"message": "Sentiment Analysis Ready"}

@router.post("/feature-1/sentiment")
async def analyze_sentiment(request: dict):
    try:
        text = request.get("text", "")
        if not text:
            return {"sentiment": "Neutral", "confidence": "0%", "tone": "Neutral"}
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Analyze the sentiment of this text and respond in JSON format with exactly these fields:
        {{"sentiment": "Positive/Negative/Neutral", "confidence": "XX%", "tone": "specific tone description"}}
        
        Text: {text}"""
        
        response = model.generate_content(prompt)
        import json
        try:
            result = json.loads(response.text)
            return result
        except:
            return {"sentiment": "Neutral", "confidence": "75%", "tone": "Informative"}
    except Exception as e:
        print(f"Error: {e}")
        return {"sentiment": "Neutral", "confidence": "50%", "tone": "Unknown"}