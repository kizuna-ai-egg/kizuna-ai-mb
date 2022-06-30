import traceback
from urllib import response
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

import urllib3
import json

from settings import OAuth2Settings, get_github

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


@app.get("/")
async def root():
    return {"message": "Hello World"}

# github oauth callback
@app.get("/github/callback", status_code=status.HTTP_200_OK)
async def github_callback(code: str, state: str, settings: OAuth2Settings = Depends(get_github)):
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

        return user_info

    except:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail='Internel Server Error'
        )