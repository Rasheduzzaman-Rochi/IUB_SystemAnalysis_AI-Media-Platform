from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import urllib.parse

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 

if not api_key:
    print("⚠️ API Key missing! Check .env file.")
else:
    genai.configure(api_key=api_key)

router = APIRouter()

class RecRequest(BaseModel):
    user_interests: list[str]
    available_articles: list[str]

@router.post("/feature-2/recommend")
async def get_recommendations(req: RecRequest):
    # Use gemini-pro for stability
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Act as a news recommendation engine.
    User Interests: {req.user_interests}
    
    Task: Generate 3 realistic news headlines matching these interests.
    
    For the "image_prompt" field, write a short, visual description of the headline (e.g., "futuristic ai robot in server room", "cricket stadium full of fans").
    
    Return JSON with this EXACT format:
    {{
        "recommended_articles": [
            {{
                "id": 1,
                "title": "Headline Here",
                "category": "Technology",
                "source": "TechDaily",
                "time": "2h ago",
                "snippet": "A short 1-line summary of the news...",
                "image_prompt": "visual description here"
            }}
        ]
    }}
    Output ONLY Valid JSON.
    """

    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        
        # --- IMAGE GENERATION TRICK ---
        # We use pollinations.ai to generate real images on the fly based on the prompt
        for article in data.get("recommended_articles", []):
            encoded_prompt = urllib.parse.quote(article.get("image_prompt", "news"))
            article["image"] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=400&nologo=true"
            
        return data
    
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # Fallback Data
        return {
            "recommended_articles": [
                {
                    "id": 1, 
                    "title": "AI Service Unavailable (Using Backup)", 
                    "category": "System", 
                    "source": "Local", 
                    "time": "Now", 
                    "snippet": "Please check your terminal logs for error details.",
                    "image": "https://placehold.co/600x400/1e293b/FFF?text=Error"
                }
            ]
        }