from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from applications.users.shemas import BaseFields, RegisterUserFields

from database.session_dependencies import get_async_session

from applications.users.models import User



router_restaurants = APIRouter()
router_users = APIRouter()
### ДЛЯ ЮЗЕРОВ
async def create_user_in_db(email, name, password, session):
    new_user = User(email=email, hashed_password=password, name=name)
    session.add(new_user)
    await session.commit()

### ДЛЯ ЮЗЕРОВ
@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def creat_user(new_user: RegisterUserFields, session: AsyncSession = Depends(get_async_session)) -> BaseFields:
    print(new_user)
    await create_user_in_db(new_user.email, new_user.name, new_user.password,session)

    return new_user
