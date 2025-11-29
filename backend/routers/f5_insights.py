from fastapi import APIRouter

router = APIRouter()

@router.get("/feature-5")
async def feature_five_test():
    return {"message": "Feature 5 (Insights) is connected!"}