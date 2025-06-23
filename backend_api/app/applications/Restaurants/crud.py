from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func, or_
import math

from applications.Restaurants.schemas import SearchParamsSchema, SortEnum, SortByEnum

from applications.Restaurants.models_restaurants import Restaurants


async def create_restaurant_in_db(restaurant_uuid, name, description, menu, feedback, main_image, images, session) -> Restaurants:
    new_restaurant = Restaurants(
        uuid_data=restaurant_uuid,
        name=name.strip(),
        description=description.strip(),
        menu=menu,
        feedback=feedback,
        main_image=main_image,
        images=images,
    )
    session.add(new_restaurant)
    await session.commit()
    return new_restaurant


async def get_restaurants_data(params: SearchParamsSchema, session: AsyncSession):
    query = select(Restaurants)
    count_query = select(func.count()).select_from(Restaurants)

    order_direction = asc if params.order_direction == SortEnum.ASC else desc

    # if params.q:
    if params.q:
        if params.use_sharp_q_filter:

            cleaned_query = params.q.strip().lower()
            search_fields = [Restaurants.name, Restaurants.description]
            search_condition = or_(*[func.lower(field) == cleaned_query for field in search_fields])

            query = query.filter(search_condition)
            count_query = count_query.filter(search_condition)




    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)
    result = await session.execute(query)
    result_count = await session.execute(count_query)
    total = result_count.scalar()
    return {
        "items": result.scalars().all(),
        "total": total,
        'page': params.page,
        'limit': params.limit,
        'pages': math.ceil(total / params.limit)
    }
