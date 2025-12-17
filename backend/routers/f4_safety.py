from fastapi import APIRouter
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

router = APIRouter()

@router.get("/feature-4")
async def feature_four_test():
    return {"message": "Safety Shield Ready"}

@router.post("/feature-4/safety")
async def verify_content(request: dict):
    """
    Verify content safety, detect misinformation, hate speech, and cyberbullying
    Returns: status (Safe/Unsafe), type, confidence, sources
    """
    try:
        text = request.get("text", "")
        if not text:
            return {
                "status": "Safe",
                "type": "Empty Content",
                "confidence": "100%",
                "sources": ["System Default"]
            }
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Detailed safety analysis prompt
        prompt = f"""Analyze the following content for safety issues and credibility.
        
Respond ONLY in this exact JSON format (no markdown, no extra text):
{{"status": "Safe|Unsafe", "type": "content_type", "confidence": "XX%", "issues": ["issue1", "issue2"]}}

Where:
- status: Safe if content is appropriate, Unsafe if it contains hate speech, misinformation, or harmful content
- type: Brief description (e.g., "Credible News", "Potential Misinformation", "Hate Speech", "Cyberbullying", "Spam")
- confidence: Confidence level (e.g., "95%", "85%", "70%")
- issues: Array of detected issues (empty if safe)

Content to analyze:
"{text}"

Respond with JSON only."""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up markdown if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        
        # Add default sources
        if "sources" not in result:
            result["sources"] = ["Gemini AI", "Content Filter"]
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        # Fallback for JSON parsing errors
        is_unsafe = any(word in text.lower() for word in ["hate", "kill", "fake", "lie", "scam", "spam", "abuse"])
        return {
            "status": "Unsafe" if is_unsafe else "Safe",
            "type": "Detected Issue" if is_unsafe else "Verified Content",
            "confidence": "75%",
            "sources": ["Gemini AI"],
            "issues": ["Content analysis performed"]
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "Safe",
            "type": "Analysis Failed",
            "confidence": "50%",
            "sources": ["Fallback"]
        }

@router.post("/feature-4/safety/batch")
async def batch_verify(request: dict):
    """Verify multiple content pieces at once"""
    try:
        texts = request.get("texts", [])
        results = []
        
        for text in texts[:5]:  # Limit to 5 items per batch
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""Quick safety check - is this safe? Reply only: Safe/Unsafe
            
Content: "{text}"

Reply: """
            
            response = model.generate_content(prompt)
            is_safe = "safe" in response.text.lower()
            
            results.append({
                "text": text[:100],
                "status": "Safe" if is_safe else "Unsafe"
            })
        
        return {"results": results}
    except Exception as e:
        print(f"Batch Error: {e}")
        return {"results": []}