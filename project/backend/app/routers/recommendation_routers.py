from fastapi import APIRouter
from app.services.recommendation_service import get_recommended_restaurants_for_user

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.get("/{user_id}")
def get_recommendations(user_id: int):
    return get_recommended_restaurants_for_user(user_id)