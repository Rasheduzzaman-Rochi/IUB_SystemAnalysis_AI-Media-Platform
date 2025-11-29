from fastapi import APIRouter

router = APIRouter()

@router.get("/feature-3")
async def feature_three_test():
    return {"message": "Feature 3 (Translation) is connected!"}