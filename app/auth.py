import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

class AuthHandler:
    @staticmethod
    def get_password_hash(password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
