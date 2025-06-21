from pydantic import BaseModel, Field


class FeedbackBase(BaseModel):
    name: str = Field(description="Restaurant name", examples=["Япіко"])
    feedback: str = Field(description="feedback", examples=["Ресторан з японською та італійською кухнею"])


class FeedbackCreate(FeedbackBase):
    pass
