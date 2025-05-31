from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import httpx


router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/')
async def index(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('index.html', context=context)
    return response


@router.get('/login')
@router.post('/login')
async def login(request: Request, user_email: str= Form(''), password: str= Form('')):
    print(F'{user_email}')
    print(F'{password}')

    users_tokens = await login_user(user_email, password)
    access_token = users_tokens.get('access_token')
    user = None
    if access_token:
        user = await get_user_info(access_token)
    context = {'request': request, "user": user}
    response = templates.TemplateResponse('login.html', context=context)
    return response



async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url='http://backend_api:9999/api/auth/login',
            data={"username":user_email,"password":password}
        )
    print(response.json())
    return response.json()



async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url='http://backend_api:9999/api/auth/get_my_info',
            headers={"Authorization": f'Bearer {access_token}'}

        )
        print(response.json())
        return response.json()
