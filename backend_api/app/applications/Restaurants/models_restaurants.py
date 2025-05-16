import uuid
from datetime import datetime

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database.base_models import Base


class Restaurants(Base):
    __tablename__ = "Restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    uuid_data: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(Text)
    menu: Mapped[str] = mapped_column(Text)
    feedback: Mapped[str] = mapped_column(Text)
