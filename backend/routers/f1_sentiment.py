from fastapi import APIRouter
import google.generativeai as genai
import os
import json
import re
from database import SessionLocal, ActivityLog

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
            result = {"sentiment": "Neutral", "confidence": "0%", "tone": "Neutral"}
            # Log activity even for empty input
            try:
                db = SessionLocal()
                log = ActivityLog(feature="sentiment", input_text=text[:256], output_result=json.dumps(result))
                db.add(log)
                db.commit()
                db.close()
            except Exception as e:
                print(f"Log error (empty input): {e}")
            return result
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Analyze the sentiment of this text in ONE line JSON format:
{{"sentiment":"Positive","confidence":"85%","tone":"Enthusiastic"}}

Only respond with valid JSON, no other text.

Text to analyze: {text}"""
        
        response = model.generate_content(prompt)
        
        try:
            # Extract JSON from response
            response_text = response.text.strip()
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                # Log activity
                try:
                    db = SessionLocal()
                    log = ActivityLog(feature="sentiment", input_text=text[:256], output_result=json.dumps(result))
                    db.add(log)
                    db.commit()
                    db.close()
                except Exception as e:
                    print(f"Log error: {e}")
                return result
            else:
                result = {"sentiment": "Neutral", "confidence": "75%", "tone": "Informative"}
                try:
                    db = SessionLocal()
                    log = ActivityLog(feature="sentiment", input_text=text[:256], output_result=json.dumps(result))
                    db.add(log)
                    db.commit()
                    db.close()
                except Exception as e:
                    print(f"Log error: {e}")
                return result
        except Exception as parse_error:
            print(f"Parse error: {parse_error}")
            print(f"Response text: {response.text}")
            # Fallback: try to infer sentiment from text
            text_lower = text.lower()
            if any(word in text_lower for word in ['love', 'great', 'amazing', 'excellent', 'wonderful', 'awesome', 'fantastic']):
                result = {"sentiment": "Positive", "confidence": "70%", "tone": "Enthusiastic"}
            elif any(word in text_lower for word in ['hate', 'terrible', 'awful', 'bad', 'horrible', 'worst', 'disgusting']):
                result = {"sentiment": "Negative", "confidence": "70%", "tone": "Frustrated"}
            else:
                result = {"sentiment": "Neutral", "confidence": "60%", "tone": "Informative"}
            try:
                db = SessionLocal()
                log = ActivityLog(feature="sentiment", input_text=text[:256], output_result=json.dumps(result))
                db.add(log)
                db.commit()
                db.close()
            except Exception as e:
                print(f"Log error (fallback): {e}")
            return result
    except Exception as e:
        print(f"Error: {e}")
        result = {"sentiment": "Neutral", "confidence": "50%", "tone": "Unknown"}
        try:
            db = SessionLocal()
            log = ActivityLog(feature="sentiment", input_text=str(request)[:256], output_result=json.dumps(result))
            db.add(log)
            db.commit()
            db.close()
        except Exception as le:
            print(f"Log error (exception): {le}")
        return result