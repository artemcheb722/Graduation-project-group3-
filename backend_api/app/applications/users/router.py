from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from applications.auth.password_handler import PasswordEncrypt
from applications.users.models import User
from applications.users.shemas import BaseFields, RegisterUserFields
from database.session_dependencies import get_async_session

router_users = APIRouter()


async def create_user_in_db(email, name, password, session: AsyncSession):
    hashed_password = await PasswordEncrypt.get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, name=name)
    session.add(new_user)
    await session.commit()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def creat_user(new_user: RegisterUserFields, session: AsyncSession = Depends(get_async_session)) -> BaseFields:
    print(new_user)
    await create_user_in_db(new_user.email, new_user.name, new_user.password, session)

    return new_user
