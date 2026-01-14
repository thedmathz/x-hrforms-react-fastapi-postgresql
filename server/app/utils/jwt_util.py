import jwt

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError

from app.core.config import settings
from app.utils.response_util import response_api

refresh_secret  = settings.SECRET_KEY
access_secret   = settings.ACCESS_SECRET_KEY

# jwt (for frontend token)
async def jwt_encode(payload, is_refresh: bool = False): 
    secret = refresh_secret if is_refresh else access_secret
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)

async def jwt_decode(token, is_refresh: bool = False): 
    secret = refresh_secret if is_refresh else access_secret
    return jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])

async def jwt_check(token, is_refresh: bool = False):
    secret = refresh_secret if is_refresh else access_secret
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except InvalidSignatureError:
        response_api(401, "Unknown signature", "Unauthorized")
    except ExpiredSignatureError:
        response_api(401, "Token has expired", "Unauthorized")
    except InvalidTokenError:
        response_api(401, "Invalid token", "Unauthorized")