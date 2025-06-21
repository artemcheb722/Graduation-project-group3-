from pydantic import BaseModel, Field


class RestaurantSchema(BaseModel):
    id: int
    name: str
    description: str
    menu: str
    feedback: str
    main_image: str
    images: list[str]


