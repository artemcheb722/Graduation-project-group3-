from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from applications.Restaurants.models_restaurants import Restaurants
from applications.Restaurants.schemas import RestaurantBase, RestaurantCreate
from database.session_dependencies import get_async_session

from applications.feedback.models_feedback import Feedback
from applications.feedback.schemas import FeedbackCreate

router_feedback = APIRouter()


async def create_feedback_in_db(name, feedback, session):
    new_feedback = Restaurants(name=name, feedback=feedback)
    session.add(new_feedback)
    await session.commit()


@router_feedback.post("/create", status_code=status.HTTP_201_CREATED)
async def create_feedback(
    new_feedback: FeedbackCreate, session: AsyncSession = Depends(get_async_session)
) -> RestaurantBase:
    await create_feedback_in_db(
        new_feedback.name, new_feedback.feedback, session
    )
    return new_feedback
