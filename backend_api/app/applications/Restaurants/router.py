from typing import Annotated
from fastapi import APIRouter, Depends, status, Body, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from services.s3.s3 import s3_storage
from applications.Restaurants.models_restaurants import Restaurants
from database.session_dependencies import get_async_session
import uuid
from sqlalchemy import String, Text
from applications.Restaurants.crud import create_restaurant_in_db, get_restaurants_data, get_restaurant_by_pk
from applications.Restaurants.schemas import RestaurantSchema, SearchParamsSchema
from applications.auth.security import admin_required
from applications.users.models import User
from sqlalchemy import select
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
        comments: str = Body(max_lenght=2500),
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
                                                        comments=comments, detailed_description=detailed_description,
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