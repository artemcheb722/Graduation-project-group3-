from applications.Restaurants.models_restaurants import Restaurants


async def create_restaurant_in_db(restaurant_uuid, name, description, menu, feedback, main_image, images, session) -> Restaurants:
    new_restaurant = Restaurants(
        uuid_data=restaurant_uuid,
        name=name,
        description=description,
        menu=menu,
        feedback=feedback,
        main_image=main_image,
        images=images,
    )
    session.add(new_restaurant)
    await session.commit()
    return new_restaurant

    pass