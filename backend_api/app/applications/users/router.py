import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from applications.users.crud import create_user_in_db, get_user_by_email
from applications.users.crud import create_user_in_db, get_user_by_email, activate_user_account
from applications.users.shemas import BaseUserInfo, RegisterUserFields
from database.session_dependencies import get_async_session

router_users = APIRouter()
@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: RegisterUserFields, session: AsyncSession = Depends(get_async_session)) -> BaseUserInfo:
    user = await get_user_by_email(new_user.email, session)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Already exists')
    created_user = await create_user_in_db(new_user.email, new_user.name, new_user.password, session)

    return created_user


@router_users.get('/verify/{user_uuid}')
async def verify_user(user_uuid: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    await activate_user_account(user_uuid, session)
    return {"Status": "activated"}