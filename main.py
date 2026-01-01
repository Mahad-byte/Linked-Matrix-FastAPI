from fastapi import FastAPI
from dotenv import load_dotenv
from database import init
from api.router import api_router

load_dotenv()

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    return {"text":"Hello World"}

@app.on_event("startup")
async def app_init():
    await init()
    # await create_test()