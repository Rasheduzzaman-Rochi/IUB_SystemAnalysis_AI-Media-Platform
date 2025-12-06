from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 

if api_key:
    genai.configure(api_key=api_key)

router = APIRouter()

# --- MOCK DATABASE (Real News er moto) ---
# Amra dhore nicchi ei news gulo amader database e ache.
# AI er kaj hobe eikhan theke user er jonno best gulo select kora.
ALL_ARTICLES = [
    {"id": 101, "category": "Technology", "title": "SpaceX Starship Successfully Reaches Orbit", "source": "TechCrunch", "time": "1h ago", "image_prompt": "SpaceX rocket launching into space realistic"},
    {"id": 102, "category": "Technology", "title": "Apple Vision Pro 2: Leaked Features Revealed", "source": "The Verge", "time": "3h ago", "image_prompt": "Futuristic VR headset apple style"},
    {"id": 103, "category": "Technology", "title": "Python 4.0: Rumors vs Reality", "source": "RealPython", "time": "5h ago", "image_prompt": "Python programming code on computer screen matrix style"},
    {"id": 104, "category": "Sports", "title": "Argentina Wins Copa America in Thrilling Final", "source": "ESPN", "time": "2h ago", "image_prompt": "Lionel Messi holding trophy stadium crowd"},
    {"id": 105, "category": "Sports", "title": "Cricket World Cup 2027 Hosts Announced", "source": "ICC News", "time": "6h ago", "image_prompt": "Cricket stadium panorama with flags"},
    {"id": 106, "category": "Finance", "title": "Bitcoin Hits New All-Time High at $80k", "source": "Bloomberg", "time": "30m ago", "image_prompt": "Bitcoin golden coin chart background"},
    {"id": 107, "category": "Finance", "title": "Global Recession Fears: What Experts Say", "source": "Financial Times", "time": "4h ago", "image_prompt": "Stock market chart crashing red arrows"},
    {"id": 108, "category": "Health", "title": "New Vaccine Shows Promise Against Malaria", "source": "WHO News", "time": "1d ago", "image_prompt": "Scientist in lab looking at microscope"},
    {"id": 109, "category": "Health", "title": "Top 10 Foods for Better Mental Health", "source": "Healthline", "time": "8h ago", "image_prompt": "Healthy food fruits and vegetables on table"},
    {"id": 110, "category": "Politics", "title": "UN Summit Discusses Climate Change Action", "source": "BBC News", "time": "2h ago", "image_prompt": "United Nations flags waving blue sky"},
    {"id": 111, "category": "Gaming", "title": "GTA VI Trailer Breaks YouTube Records", "source": "IGN", "time": "12h ago", "image_prompt": "Vice City style sunset sports car"},
    {"id": 112, "category": "Gaming", "title": "Esports Now Officially an Olympic Sport", "source": "Kotaku", "time": "1d ago", "image_prompt": "Esports arena gamers with headsets"},
]

class RecRequest(BaseModel):
    user_interests: list[str]
    available_articles: list[str]

@router.post("/feature-2/recommend")
async def get_recommendations(req: RecRequest):
    model = genai.GenerativeModel('gemini-2.5-flash')

    # AI ke amra Database er sob Title dicchi
    # AI ke bolchi: "Eigulor moddhe konta user er valo lagbe?"
    
    available_titles = [f"ID {a['id']}: {a['title']} ({a['category']})" for a in ALL_ARTICLES]
    available_titles_str = "\n".join(available_titles)

    prompt = f"""
    Act as a Recommendation System.
    
    USER PROFILE (Interests): {req.user_interests}
    
    DATABASE OF ARTICLES:
    {available_titles_str}
    
    TASK:
    Select the top 3 articles from the database that match the user's interests best.
    If no direct match is found, pick the most popular/general ones.
    
    Return JSON with this EXACT format:
    {{
        "selected_ids": [101, 104, 110]
    }}
    Output ONLY Valid JSON.
    """

    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result_ids = json.loads(clean_text).get("selected_ids", [])
        
        # Filter the full article objects based on the IDs selected by AI
        recommended_articles = [article for article in ALL_ARTICLES if article["id"] in result_ids]
        
        # Add Images dynamically (using the pre-defined prompt)
        for article in recommended_articles:
            import urllib.parse
            encoded_prompt = urllib.parse.quote(article["image_prompt"])
            article["image"] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=400&nologo=true"
            article["snippet"] = f"Recommended because you like {article['category']}..." # Simple snippet

        return {"recommended_articles": recommended_articles}
    
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # Fallback: Just return the first 3 articles
        return {"recommended_articles": ALL_ARTICLES[:3]}