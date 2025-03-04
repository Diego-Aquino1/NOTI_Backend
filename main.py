from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from routers.res_users import api_res_users
from jose import jwt, JWTError
from datetime import datetime, timedelta,timezone

#variable en servidor
SECRETE_KEY="Wo4OHExa25nMnMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDEyODA4NDEwNzU2MjUwMzQwMjAiLCJlbWFpbCI6ImRzYjMyMW1wQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiWmpVY1Eyd3JkLUdzY3F2Y2dqci1BQSIsIm5vbmNlIjoiUFp2SGhsX2tUTGR1Sktmem80LW9qdyIsImlhdCI6MTYxMTY5MjA2NywiZXhwIjoxNjExNjk1NjY3fQ.kNFbqjtJO2HKsSX-jt967MLi2xjeRH4W9JsA4yPQDQEgrHqa3BX6PVFJCBjq-Fn7vmlTT1lUcElVPwtvcBUV8Z4I7dCuWKcTxTt6R8501f1I2X0tQeEu_zfg-ianzOlQkg3KvLT_D-oaIfNkoU7jAt4Mywe6xHiDKszlA6KE8T6PLV_VeiCJGvciLbPW7DhKiuL-kfTjhHoZ6_XHeruR6rb_psZNvH5t-D3Yjc27EwH0_Wumcl1GjN20eF2xO-"
TOKEN_SECONDS_EXP = 20
db_users ={
    "gregory": {
        "id": 0,
        "username": "gregory",
        "password": "4321#hash"
    },

    "sol": {
        "id": 1,
        "username": "sol",
        "password": "1234#hash"
    }
}

app = FastAPI()

app.include_router(api_res_users.router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jinja2_template = Jinja2Templates(directory="templates")

def get_user(username:str, db: list):
    if username in db:
        return db[username]
    
def authenticate_user(password: str, password_plane: str):
    password_clean = password.split("#")[0]
    if password_plane == password_clean:
        return True
    return False
def create_token(data: list):
    data_token =data.copy()
    data_token["exp"]=datetime.now(timezone.utc) + timedelta(seconds=TOKEN_SECONDS_EXP)
    token_jwt = jwt.encode(data_token, key=SECRETE_KEY, algorithm="HS256")
    return token_jwt
""""
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def testing():
    return {"hola": "Si corre"}
"""
@app.get("/",response_class=HTMLResponse)
def root(request: Request):
    return jinja2_template.TemplateResponse("index.html", {"request":request})

@app.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return jinja2_template.TemplateResponse("dashboard.html", {"request": request})

@app.post("/users/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = get_user(username, db_users)
    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail= "Username or Password No Authorization"
        )
    if not authenticate_user(user_data["password"], password):
        raise HTTPException(
            status_code=401,
            detail= "Username or Password No Authorization"
        )
    token = create_token({"username": user_data["username"]})
    return RedirectResponse (
        "/users/dashboard", 
        status_code = 302,
        headers = {"set-cookie": f"acces_token = {token}; Max-Age = {TOKEN_SECONDS_EXP} "} 
    )