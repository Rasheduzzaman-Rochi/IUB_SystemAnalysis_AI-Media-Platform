from fastapi import APIRouter
import google.generativeai as genai
import os
from database import SessionLocal, ActivityLog
import json

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
        
        result = {
            "summary": summary,
            "compression_ratio": f"{round(len(summary)/len(text)*100, 1)}%"
        }
        
        # Log activity
        try:
            db = SessionLocal()
            log = ActivityLog(
                feature="summary",
                input_text=text[:256],
                output_result=summary[:256]
            )
            db.add(log)
            db.commit()
            db.close()
        except Exception as log_err:
            print(f"Log error: {log_err}")
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        result = {"summary": "Summary generation failed", "compression_ratio": "0%"}
        
        # Log activity
        try:
            db = SessionLocal()
            log = ActivityLog(
                feature="summary",
                input_text=text[:256] if text else "empty",
                output_result="Error"
            )
            db.add(log)
            db.commit()
            db.close()
        except Exception as log_err:
            print(f"Log error: {log_err}")
        
        return result