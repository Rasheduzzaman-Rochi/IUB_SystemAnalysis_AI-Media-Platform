from fastapi import APIRouter

router = APIRouter()

@router.get("/feature-2")
async def feature_two_test():
    return {"message": "Feature 2 (Recommendation) is connected!"}