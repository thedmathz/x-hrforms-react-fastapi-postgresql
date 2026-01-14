import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, Request
from fastapi.security.utils import get_authorization_scheme_param
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError

from app.utils.response_util import response_api
from app.utils.jwt_util import jwt_check
from app.core.config import settings

from app.repositories.refresh_token_repository import RefreshTokenRepository

refresh_token_repository = RefreshTokenRepository()

class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        auth: str = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(auth)
        if not auth or scheme.lower() != "bearer" or not token:
            raise response_api(401)
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=token)

# dependency instance
security = CustomHTTPBearer()

async def get_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return credentials.credentials

async def get_current_user(token: str = Depends(get_token)):
    
    # decode and verify token
    payload = await jwt_check(token)
    
    # get token payload 
    user_id = payload.get("sub")
    
    return user_id 

async def get_refresh_identity(token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
    
    # decode and verify token
    payload = await jwt_check(token, is_refresh=True)
    
    user_id = int(payload.get("sub"))
    
    return {
        "user_id"       : user_id,
        "refresh_token" : token, 
        "db" : db, 
    } 