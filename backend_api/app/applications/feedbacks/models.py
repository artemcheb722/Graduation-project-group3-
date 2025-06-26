from database.base_models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import ForeignKey, Text

class Feedbacks(Base):
    __tablename__ = "Feedbacks"


    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("Restaurants.id"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    user = relationship("User", backref="feedbacks")
    restaurant = relationship("Restaurants", backref="feedbacks")

    def __str__(self):
        return f"Feedback from User {self.user_id} to Restaurant {self.restaurant_id}"