from fastapi import APIRouter

router = APIRouter()

@router.get("/feature-4")
async def feature_four_test():
    return {"message": "Feature 4 (Safety) is connected!"}