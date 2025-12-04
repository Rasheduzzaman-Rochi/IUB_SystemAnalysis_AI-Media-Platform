from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import all routers
from routers import f1_sentiment, f2_recommend, f3_translate, f4_safety, f5_insights, f6_summary
import uvicorn

app = FastAPI()

# IMPORTANT: CORS SETUP (For UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect Routers
app.include_router(f1_sentiment.router)
app.include_router(f2_recommend.router)
app.include_router(f3_translate.router)
app.include_router(f4_safety.router)
app.include_router(f5_insights.router)
app.include_router(f6_summary.router)

@app.get("/")
def home():
    return {"status": "MediaMind Backend Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)