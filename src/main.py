from datetime import timedelta
import traceback
import urllib3
import json

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from settings import OAuth2Settings, get_github
from schemas import Token, UserIn
import db, service, security


# CORS white list
origins = [

]

app = FastAPI()
http_client = urllib3.PoolManager()

# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup():
    await db.database.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# github oauth callback
@app.get("/github/callback", status_code=status.HTTP_200_OK)
async def github_callback(code: str, state: str, settings: OAuth2Settings = Depends(get_github), db: Session = Depends(db.get_db)):
    user_info = None

    try:
        token = http_client.request(
        'POST', 
        'https://github.com/login/oauth/access_token',
        headers={
            'accept': 'application/json'
        },
        fields={
            'client_id': settings.client_id,
            'client_secret': settings.client_secret,
            'code': code
        }
        )

        token = json.loads(token.data.decode('utf-8'))

        user_info = http_client.request(
            'GET',
            'https://api.github.com/user',
            headers={
                'accept': 'application/json',
                'Authorization': 'token {}'.format(token['access_token'])
            }
        )

        user_info = json.loads(user_info.data.decode('utf-8'))

    except:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail='Faild to request github api'
        )

    
    if user_info:
        user = UserIn(id=str(user_info['id']), nick_name=user_info['login'], avatar_url=user_info['avatar_url'], type='github')
        service.login(user, db)

        access_token = security.create_token(
            payload={
                'id': user_info['id'],
                'nick_name': user_info['login'],
                'type': 'github'
            },
            expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRED_MINUTES)
        )

        refresh_token = security.create_token(
            payload={
                'id': user_info['id'],
                'nick_name': user_info['login'],
                'type': 'github'
            },
            expires_delta=timedelta(days=security.REFRESH_TOKEN_EXPIRED_DAYS)
        )

        return Token(token_type='Bearer', access_token=access_token, refresh_token=refresh_token)
    else:
        raise HTTPException(
            status_code=500,
            detail='Faild to get user information'
        )
