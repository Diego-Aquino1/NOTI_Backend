from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

from routers.geo_location import api_geo_location
from routers.res_users import api_res_users

app = FastAPI()

app.include_router(api_res_users.router)
app.include_router(api_geo_location.router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def testing():
    return {"hola": "Si corre"}

