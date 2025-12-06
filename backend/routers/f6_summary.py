from fastapi import APIRouter
import google.generativeai as genai
import os

router = APIRouter()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY", "your-key-here")
genai.configure(api_key=api_key)

@router.get("/feature-6")
async def feature_six_test():
    return {"message": "Summarization Ready"}

@router.post("/feature-6/summary")
async def summarize_text(request: dict):
    try:
        text = request.get("text", "")
        if not text or len(text) < 50:
            return {"summary": text}
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Summarize this text in 2-3 sentences. Keep it concise and clear:
        
        {text}"""
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        return {
            "summary": summary,
            "compression_ratio": f"{round(len(summary)/len(text)*100, 1)}%"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"summary": "Summary generation failed", "compression_ratio": "0%"}