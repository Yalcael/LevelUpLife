from fastapi import APIRouter, Depends

from leveluplife.controllers.rating import RatingController
from leveluplife.dependencies import get_rating_controller
from leveluplife.models.rating import RatingCreate
from leveluplife.models.view import RatingView

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=RatingView, status_code=201)
async def create_rating(
    rating: RatingCreate,
    rating_controller: RatingController = Depends(get_rating_controller),
) -> RatingView:
    return RatingView.model_validate(await rating_controller.create_rating(rating))
