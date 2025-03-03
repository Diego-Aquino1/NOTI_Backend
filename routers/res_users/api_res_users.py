from fastapi import Request, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from routers.res_users.controllers.get_all_users_controller import UserAllController

router = APIRouter(prefix="/user")

@router.get("/")
def test():
    return jsonable_encoder({"rpta", "Usuarios"})


@router.get("/all", status_code = 200)
# def get_roles(auth = Auth()):
def get_roles():
    controller = UserAllController()
    # return jsonable_encoder(controller.run(auth))
    return jsonable_encoder(controller.run())