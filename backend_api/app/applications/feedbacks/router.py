from fastapi import APIRouter, status, Depends, HTTPException, Form, Request
from applications.feedbacks.schemas import FeedbackCreate, FeedbackRead
from database.session_dependencies import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from applications.Restaurants.models_restaurants import Restaurants
from applications.users.models import User
from applications.feedbacks.models import Feedbacks
from sqlalchemy import select
from typing import List
from frontend.app.backend_api.api import get_current_user_with_token


router_feedbacks = APIRouter()


@router_feedbacks.post("/create")
async def create_feedback_from_form(
    request: Request,
    comment: str = Form(...),
    restaurant_id: int = Form(...),
    user: dict = Depends(get_current_user_with_token),
    session: AsyncSession = Depends(get_async_session)
):
    restaurant = await session.get(Restaurants, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db_user = await session.get(User, user["id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    feedback = Feedbacks(
        user_id=user["id"],
        restaurant_id=restaurant_id,
        comment=comment
    )

    session.add(feedback)
    await session.commit()

    return RedirectResponse(
        url=f"/restaurant/{restaurant_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router_feedbacks.get(
    "/restaurant/{restaurant_id}",
    response_model=List[FeedbackRead]
)
async def list_feedbacks_for_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_async_session)
):

    result = await session.execute(
        select(Feedbacks, User.name)
        .join(User, Feedbacks.user_id == User.id)
        .where(Feedbacks.restaurant_id == restaurant_id)
    )

    return [
        FeedbackRead(
            id=feedback.id,
            user_name=user_name,
            comment=feedback.comment
        )
        for feedback, user_name in result.all()
    ]
