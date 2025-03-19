from fastapi import Request, APIRouter
from sqlalchemy.orm import Session
from database import get_session
from fastapi.encoders import jsonable_encoder
from routers.geo_location.controllers.find_location_controller import FindLocationController
from routers.geo_location.controllers.massive_find_locations_controller import MassiveFindLocationsController
from routers.geo_location.schemas.location_schemas import LocationRequest


router = APIRouter(prefix="/location")


@router.post("/find", status_code = 200)
def register(data: LocationRequest):
    controller = FindLocationController()
    return jsonable_encoder(controller.run(data))

@router.post("/massive_find", status_code = 200)
def register(data: list[LocationRequest]):
    controller = MassiveFindLocationsController()
    return jsonable_encoder(controller.run(data))