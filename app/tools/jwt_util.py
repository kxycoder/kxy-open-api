from datetime import datetime, timedelta
from jose import jwt

from app.config import config

class JwtUtil():
    def create_jwt_token(data: dict,TOKEN_EXPIRE_MINUTES:int=1440,keep=False) -> str:
        """生成JWT"""
        to_encode = data.copy()
        if keep=='1':
            TOKEN_EXPIRE_MINUTES = 43200 # 30天
        expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
        return encoded_jwt