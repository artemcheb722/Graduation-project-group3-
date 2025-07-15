from typing import Annotated
from fastapi import APIRouter, Depends, status, Body, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.s3.s3 import s3_storage
from applications.Restaurants.models_restaurants import Restaurants
from database.session_dependencies import get_async_session
import uuid
from sqlalchemy import  Text
from applications.Restaurants.crud import create_restaurant_in_db, get_restaurants_data, get_restaurant_by_pk, create_comment
from applications.Restaurants.schemas import RestaurantSchema, SearchParamsSchema, CommentResponse, CommentCreate
from applications.users.models import User
from sqlalchemy import select
from applications.Restaurants.models_restaurants import RestaurantComments
from applications.auth.security import get_current_user
from fastapi import Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER




router_restaurants = APIRouter()


@router_restaurants.post("/create",
                         # dependencies=[Depends(admin_required)]
                         )
async def create_restaurant(
        main_image: UploadFile,
        images: list[UploadFile] = None,
        name: str = Body(max_lenght=50),
        city: str = Body(max_lenght=300),
        description: str = Body(Text),
        menu: str = Body(Text),
        detailed_description: str = Body(Text),
        session: AsyncSession = Depends(get_async_session)
) -> RestaurantSchema:
    restaurant_uuid = uuid.uuid4()
    main_image = await s3_storage.upload_product_image(main_image, restaurant_uuid=restaurant_uuid)
    images = images or []
    images_urls = []
    for image in images:
        url = await s3_storage.upload_product_image(image, restaurant_uuid=restaurant_uuid)
        images_urls.append(url)

    created_restaurant = await  create_restaurant_in_db(restaurant_uuid=restaurant_uuid, name=name, city=city,
                                                        description=description, menu=menu,
                                                        detailed_description=detailed_description,
                                                        main_image=main_image, images=images_urls,
                                                        session=session)

    return created_restaurant


@router_restaurants.get('/by_city')
async def get_restaurants_by_city(city: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Restaurants).where(Restaurants.city == city)
    )
    restaurants = result.scalars().all()
    return {
        "items": restaurants,
        "total": len(restaurants),
    }

@router_restaurants.get('/{pk}')
async def get_product(pk: int, session: AsyncSession = Depends(get_async_session), ) -> RestaurantSchema:
    product = await get_restaurant_by_pk(pk, session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with pk #{pk} not found")
    return product


@router_restaurants.get('/')
async def get_restaurants(params: Annotated[SearchParamsSchema, Depends()],
                          session: AsyncSession = Depends(get_async_session)):
    result = await get_restaurants_data(params, session)
    return result


@router_restaurants.post('/create_comments', response_model=CommentResponse)
async def post_comments(
    feedback: CommentCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    restaurant = await get_restaurant_by_pk(feedback.restaurant_id, session)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Ресторан не знайдено")

    comment = await create_comment(
        user_id=user.id,
        restaurant_id=feedback.restaurant_id,
        feedback=feedback.text,
        session=session
    )

    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        restaurant_id=comment.restaurant_id,
        text=comment.feedback,  # ⚠️ или .text если ты переименовывал
        user_name=user.name  # используем текущего юзера
    )

@router_restaurants.get("/comments/{restaurant_id}")
async def get_comments_for_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        select(RestaurantComments, User.name)
        .join(User, User.id == RestaurantComments.user_id)
        .where(RestaurantComments.restaurant_id == restaurant_id)
    )
    result = await session.execute(stmt)
    feedbacks_with_users = result.all()

    return [
        {
            "text": comment.feedback,
            "author": name
        }
        for comment, name in feedbacks_with_users
    ]