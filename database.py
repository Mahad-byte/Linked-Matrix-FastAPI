from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from models.users import User, Profile, Token
from models.project import Project, Tasks, Timeline
from models.content import Document, Comment
from models.notification import Notification


uri = "mongodb+srv://mahadnaeem416_db_user:wFpdgJLsNZM3Kbzb@cluster0.3u9vrvy.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(uri)
db = client['FastAPI']

async def init():
    await init_beanie(database=db, 
                      document_models=[
                          User, Profile, Project, Tasks, Timeline, Document, Comment, 
                          Notification, Token
                        ])
    

# async def create_test():
#     # user = User(email="mahad@example.com", password="1234", created_at=datetime.now())
#     # await user.insert()
#     user = await User.find_one(User.email == "mahad@example.com")
#     print("User: ", user)
#     profile = Profile(role="PM", user_id=user.id, picture=None) 
#     await profile.insert()
#     user.profile = profile.id
#     await user.save()

