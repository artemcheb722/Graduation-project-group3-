


from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    user_id: int
    restaurant_id: int
    comment: str

class FeedbackRead(BaseModel):
    id: int
    user_name: str
    comment: str

    class Config:
        orm_mode = True