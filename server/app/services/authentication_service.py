import datetime

from fastapi import HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi.responses import JSONResponse 
from app.repositories.authentication_repository import AuthenticationRepository
from app.models.token import Token
from app.schemas.authentication import AuthenticationLogin

from app.core.config import settings

from app.utils.response_util import response_api
from app.utils.argon2_util import argon2_verify
from app.utils.jwt_util import jwt_encode

class AuthenticationService:
    
    def __init__(self): self.repo = AuthenticationRepository()

    async def login(self, db: AsyncSession, form_request: AuthenticationLogin): 
        
        data = response_api(200) 
        
        refresh_token = '' 
        
        # validation
        if not form_request.username or not form_request.password:
            response_api(400, f'Username and password are required.', 'Invalid!')
        
        # 
        async with db.begin():
            
            # get user by username 
            row = await self.repo.get_user_by_username(db, form_request.username) 
            
            # if user not found
            if not row: 
                response_api(400, f'Invalid username or password.', 'Oops!')
            
            # if user exists, verify password
            if not argon2_verify(row['password'], form_request.password):
                response_api(400, f'Invalid username or password.', 'Oops!')
            
            # if password correct, check if user is active
            if row['status'] != 1:
                response_api(400, f'Account has been deactivated. Please contact your administrator.', 'Invalid!')
            
            # if active, generate refresh and access token
            payload = { 'sub' : str(row['user_id']) }
            
            payload['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            refresh_token = await jwt_encode(payload, True)
            
            if refresh_token:
                
                new_token = Token(
                    user_id             = row['user_id'],
                    username            = form_request.username,
                    token               = refresh_token,
                    date_started        = datetime.datetime.now(datetime.timezone.utc),
                    date_stopped        = None, 
                    date_expiration     = payload['exp'],
                    time_minute_used    = 0, 
                    time_minute_total   = settings.REFRESH_TOKEN_EXPIRE_MINUTES, 
                    is_active           = 1, 
                )
            
                await self.repo.insert_new_token(db, new_token) 
            
                payload['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = await jwt_encode(payload)
            
            data['refresh_token'] = refresh_token
            data['access_token'] = access_token
        
        response = JSONResponse(status_code=200, content=data)
    
        # Set cookie for refresh token
        response.set_cookie(
            key         = "token", 
            value       = refresh_token, 
            httponly    = True, 
            secure      = settings.ENVIRONMENT == "production", 
            samesite    = "lax", 
            max_age     = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60, 
            path        = "/",
        )
        
        return response
    
    async def me(self, db: AsyncSession, current_user_id: int): 
        
        data = response_api(200) 
        
        async with db.begin():
            
            # get user info
            user_info = await self.repo.get_user_by_user_id(db, current_user_id)
            
            data['name']        = user_info['username'] if user_info else ""
            data['user_type']   = user_info['user_type_name'] if user_info else ""
        
        return JSONResponse(status_code=200, content=data)
    
    async def refresh(self, identity: dict): 
        
        db: AsyncSession    = identity["db"]
        token: str          = identity["refresh_token"]
        user_id: int        = identity["user_id"]
        
        data = response_api(200) 
        
        async with db.begin():
        
            # get token from database
            token_row = await self.repo.get_token_by_value(db, token) 
            
            date_started        = token_row.date_started 
            date_stopped        = datetime.datetime.now(datetime.timezone.utc) 
            time_minute_used    = int((date_stopped - date_started).total_seconds() / 60) 
            is_active           = token_row.is_active
            
            # calculate time used
            if time_minute_used > token_row.time_minute_total:
                date_stopped        = token_row.date_expiration
                time_minute_used    = token_row.time_minute_total
                is_active           = 0
            
            # if token not found
            if not token_row: 
                response_api(401, 'Invalid token.', 'Unauthorized!') 
                
            # if token not active
            if is_active != 1: 
                response_api(401, 'Token expired.', 'Unauthorized!') 
            
            # update token expiration time and status if not active
            token_row.date_stopped = date_stopped
            token_row.time_minute_used = time_minute_used
            token_row.is_active = is_active

            # generate new access token
            payload = { 
                'sub' : str(user_id), 
                'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), 
            }
            data['token'] = await jwt_encode(payload)
        
        return JSONResponse(status_code=200, content=data)
    
    async def logout(self, db: AsyncSession, token: str): 
        
        data = response_api(200) 
        
        response = JSONResponse(status_code=200, content=data)
        
        async with db.begin():
        
            # get token from database
            token_row = await self.repo.get_token_by_value(db, token)
            
            if token_row:
                
                date_stopped        = datetime.datetime.now(datetime.timezone.utc)
                time_minute_used    = int((date_stopped - token_row.date_started).total_seconds() / 60)
                
                if time_minute_used > token_row.time_minute_total:
                    date_stopped        = token_row.date_expiration
                    time_minute_used    = token_row.time_minute_total
                    
                # update token as inactive
                token_row.date_stopped      = date_stopped
                token_row.time_minute_used  = time_minute_used
                token_row.is_active         = 0

            # delete cookie
            response.delete_cookie(
                key             = "token",
                httponly        = True,
                secure          = settings.ENVIRONMENT == "production", 
                samesite        = "lax"
            )
        
        return response
