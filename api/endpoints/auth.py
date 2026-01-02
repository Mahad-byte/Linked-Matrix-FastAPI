from fastapi import APIRouter, status, Depends, HTTPException
from models.users import User, Profile, Token
from jwt.exceptions import InvalidTokenError
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from utils.helpers import auth_helper, create_notification
from schemas.schema import RegisterSchema, LoginSchema, TokenSchema, ResponseSchema
from datetime import datetime


router = APIRouter()
uri = "mongodb+srv://mahadnaeem416_db_user:wFpdgJLsNZM3Kbzb@cluster0.3u9vrvy.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(uri)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterSchema):

    if payload.password != payload.confirm_password:
        return {"message": "Password and Confirm Password do not match"}

    hashed_password = auth_helper.get_password_hash(payload.password)
    created_at = datetime.now()

    # Atomic Transaction
    async with await client.start_session() as session:
        async with session.start_transaction():
            user = User(
                email=payload.email, password=hashed_password, created_at=created_at
            )
            await user.insert()

            profile = Profile(user_id=user.id, role=payload.role, picture=None)
            await profile.insert()

            await create_notification(
                user=str(user.id),
                text="User {user.email} account created",      
            )


    return ResponseSchema(message="Success")


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(payload: LoginSchema):
    user = await User.find_one(User.email == payload.email)
    print("User: ", user)
    if user is None:
        return {"message": "User does not exists"}

    if not auth_helper.verify_password(payload.password, user.password):
        return {"message": "Password does not matches"}

    access_token = auth_helper.create_access_token(user_id=str(user.id))
    token = Token(access_token=access_token, token_type="bearer", user_id=str(user.id))
    await token.insert()
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(token: str = Depends(oauth2_scheme)):
    token_doc = await Token.find_one(Token.access_token == token)
    if token_doc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found or already logged out",
        )

    await token_doc.delete()
    return ResponseSchema(message="Logged out successfully")
