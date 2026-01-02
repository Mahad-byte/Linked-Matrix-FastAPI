import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from functools import wraps

from models.notification import Notification
from models.users import User, Token


 # injects token in headers and send to get_current_user, does not hit /login API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class AuthHelper:
    def __init__(self, secret_key: str, algorithm: str, access_token_expiry: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expiry = access_token_expiry
        self.hashed_password = PasswordHash.recommended()

    def create_access_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expiry)
        payload = {"user_id": user_id, "exp": expire}
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.hashed_password.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.hashed_password.hash(password)

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme),
    ) -> User:
        # First, check if token exists in token collection for the user_id
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("user_id")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )

            # Check if a token exists for this user in the collection
            token_record = await Token.find_one({"user_id": user_id})

            if token_record is None:
                # No token found for this user, raise error
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No active session found",
                )

            # Fetch user from database
            user = await User.get(user_id)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            return user

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )


SECRET_KEY = "13f39561144d226c88119d138915b172791c4a0d8e10d8ef24b4f3115846f9f5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def init_auth_helper():
    return AuthHelper(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expiry=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


# Default helper instance for convenient reuse
auth_helper = init_auth_helper()
    

async def create_notification(*, user: str, text: str):
    notification = Notification(
        user=user,
        text=text,
        mark_read=False,
        created_at=datetime.utcnow(),
    )
    await notification.insert()
