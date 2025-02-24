from fastapi import Request, APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime

from routers.products.controllers.get_all_products_controller import ProductsAllController

router = APIRouter(prefix="/products")

# =============== GET -> Create products ===============
@router.get("/")
def get_products():
    return jsonable_encoder({"rpta", "Products"})


@router.get("/all", status_code = 200)
# def get_roles(auth = Auth()):
def get_roles():
    controller = ProductsAllController()
    # return jsonable_encoder(controller.run(auth))
    return jsonable_encoder(controller.run())