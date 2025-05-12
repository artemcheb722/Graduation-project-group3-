from pydantic import BaseModel, Field

class RestaurantBase(BaseModel):
    name: str = Field(description="Restaurant name", examples=["Япіко"])
    description: str = Field(description="description",examples=["Ресторан з японською та італійською кухнею"])
    feedback: str = Field(description="feedback",examples=["Ресторан з японською та італійською кухнею"])

class RestaurantCreate(RestaurantBase):
    pass
