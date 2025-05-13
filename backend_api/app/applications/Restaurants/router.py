from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from applications.Restaurants.schemas import RestaurantCreate, RestaurantBase
from database.session_dependencies import get_async_session
from applications.Restaurants.models_restaurants import Restaurants

router_restaurants = APIRouter()

async def create_restaurant_in_db(name, description, menu, feedback, session):
    new_restaurant = Restaurants(name=name, description=description,menu=menu, feedback=feedback)
    session.add(new_restaurant)
    await session.commit()

@router_restaurants.post("/create", status_code=status.HTTP_201_CREATED)
async def create_restaurant(new_restaurant: RestaurantCreate, session: AsyncSession = Depends(get_async_session)) -> RestaurantBase:
    await create_restaurant_in_db(new_restaurant.name, new_restaurant.description,new_restaurant.menu, new_restaurant.feedback, session)
    return new_restaurant