from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRED_MINUTES = 30
REFRESH_TOKEN_EXPIRED_DAYS = 7


def create_token(payload: dict, expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt