from passlib.context import CryptContext
from typing import Any
import datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from app.core.repositories.headhunter_repository import HeadhunterRepository, Headhunter

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Authenticator:
    def __init__(
        self, 
        secret_key: str, 
        algorithm: str, 
        access_token_expire_minutes: int,
        headhunter_repository: HeadhunterRepository,
    ) -> None:
        self._SECRET_KEY = secret_key
        self._ALGORITHM = algorithm
        self._ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        self._headhunter_repository = headhunter_repository

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict[str, Any]):
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.timezone.utc) + (self._ACCESS_TOKEN_EXPIRE_MINUTES * datetime.timedelta(minutes=1))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self._SECRET_KEY, algorithm=self._ALGORITHM)

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Headhunter:
        try:
            payload = jwt.decode(token, self._SECRET_KEY, algorithms=[self._ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        headhunter = self._headhunter_repository.get_headhunter_by_id(user_id)
        if headhunter is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        return headhunter