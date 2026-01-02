import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, Request
from functools import wraps
import inspect

from models.users import User, Token, Profile
from utils.enums import Role


class AuthHelper:
    def __init__(self, secret_key: str, algorithm: str, access_token_expiry: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expiry = access_token_expiry
        self.hashed_password = PasswordHash.recommended()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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
        self, token: str = Depends(lambda self: self.oauth2_scheme)
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


def roles_required(*allowed_roles: Role):

    async def _dependency(user: User = Depends(auth_helper.get_current_user)):
        profile = await Profile.find_one(Profile.user_id == user.id)
        if profile is None or profile.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return user

    return Depends(_dependency)


def pm_required():
    return roles_required(Role.PM)


class RoleChecker:
    
    def __init__(self, auth_helper: AuthHelper):
        self.auth_helper = auth_helper

    def required(self, *allowed_roles: Role):
        def decorator(func):
            orig_sig = inspect.signature(func)

            # Build a new signature that includes `request` (if not present) followed by
            # the original parameters. Make `current_user` optional so FastAPI doesn't
            # treat it as a required body field.
            params = []
            if "request" not in orig_sig.parameters:
                params.append(
                    inspect.Parameter(
                        "request",
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=Request,
                    )
                )

            for name, param in orig_sig.parameters.items():
                if name == "current_user" and param.default is inspect._empty:
                    param = param.replace(default=None)
                params.append(param)

            wrapper_sig = inspect.Signature(parameters=params, return_annotation=orig_sig.return_annotation)

            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                auth_header = request.headers.get("authorization")
                if not auth_header:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Missing authorization header",
                    )

                parts = auth_header.split()
                token = parts[1] if len(parts) > 1 else parts[0]

                user = await self.auth_helper.get_current_user(token=token)
                profile = await Profile.find_one(Profile.user_id == user.id)
                if profile is None or profile.role not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Operation not permitted",
                    )

                # Inject current_user and request into kwargs if the original function expects them
                if "current_user" in orig_sig.parameters:
                    kwargs["current_user"] = user
                if "request" in orig_sig.parameters:
                    kwargs["request"] = request

                return await func(*args, **kwargs)

            # Expose the constructed signature to FastAPI so it knows to provide Request
            wrapper.__signature__ = wrapper_sig

            return wrapper

        return decorator


role = RoleChecker(auth_helper)
