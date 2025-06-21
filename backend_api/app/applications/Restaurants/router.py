from fastapi import APIRouter, Depends, status, Body, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from services.s3.s3 import s3_storage
from applications.Restaurants.models_restaurants import Restaurants
from database.session_dependencies import get_async_session
import uuid

from applications.Restaurants.crud import create_restaurant_in_db

from applications.Restaurants.schemas import RestaurantSchema

router_restaurants = APIRouter()





@router_restaurants.post("/create", status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    main_image: UploadFile,
    images: list[UploadFile] = None,
    name: str = Body(max_lenght=50),
    description: str = Body(max_lenght=150),
    menu: str = Body(max_lenght=100),
    feedback: str = Body(max_lenght=120),
    session: AsyncSession = Depends(get_async_session)
) -> RestaurantSchema:
    restaurant_uuid = uuid.uuid4()
    main_image = await s3_storage.upload_product_image(main_image, restaurant_uuid=restaurant_uuid)
    images = images or []
    images_urls = []
    for image in images:
        url = await s3_storage.upload_product_image(image, restaurant_uuid=restaurant_uuid)
        images_urls.append(url)

    created_restaurant = await  create_restaurant_in_db(restaurant_uuid=restaurant_uuid, name=name, description=description, menu=menu,
                                feedback=feedback,main_image=main_image, images=images_urls, session=session)
    return created_restaurant

