from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

import db, crud, schemas, models

SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRED_MINUTES = 30
REFRESH_TOKEN_EXPIRED_DAYS = 7
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='token')

INVALID_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token',
        headers={'WWW-Authenticate': 'Bearer'}
    )

EXPIRED_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Signature has expired',
        headers={'WWW-Authenticate': 'Bearer'}
    )

def create_token(payload: dict, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def get_current_user(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(db.get_db)) -> models.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('id')
        nick_name = payload.get('nick_name')
        type = payload.get('type')
        if id is None or nick_name is None or type is None:
            raise INVALID_EXCEPTION
        
    except JWTError as e:
        if isinstance(e, ExpiredSignatureError):
            raise EXPIRED_EXCEPTION
        
    user = crud.query_user(schemas.UserIn(id=id, nick_name=nick_name, type=type, avatar_url=''), db)
    if user is None:
        raise INVALID_EXCEPTION
    
    return user