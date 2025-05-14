from fastapi import Query, APIRouter
from sqlalchemy.orm import Session
from database import get_session
from fastapi.encoders import jsonable_encoder
from routers.geo_location.controllers.find_location_controller import FindLocationController
from routers.geo_location.controllers.massive_find_locations_controller import MassiveFindLocationsController
from routers.geo_location.controllers.find_location_coordinate import FindLocationCoordinateController
from routers.geo_location.controllers.find_incident import FindIncidentController
from routers.geo_location.schemas.location_schemas import LocationRequest, LocationCoordinateRequest
from routers.geo_location.schemas.location_schemas import LocationRequest
from routers.geo_location.controllers.find_incident_for_id import GetIncidentByIdController


router = APIRouter(prefix="/location")

@router.post("/find", status_code=200)
def register(data: LocationRequest):
    controller = FindLocationController()
    return jsonable_encoder(controller.run(data))

@router.post("/massive_find", status_code=200)
def register(data: list[LocationRequest]):
    controller = MassiveFindLocationsController()
    return jsonable_encoder(controller.run(data))

@router.post("/find_by_coordinates", status_code=200)
def find_by_coordinates(data: LocationCoordinateRequest):
    controller = FindLocationCoordinateController()
    return jsonable_encoder(controller.run(data))

@router.post("/find_incidents_by_coordinates", status_code=200)
def find_incidents_by_coordinates(data: LocationCoordinateRequest):
    controller = FindIncidentController()
    return jsonable_encoder(controller.run(data))

@router.get("/incident", status_code=200)
def get_incident_by_id(id_incident: int = Query(..., description="ID del incidente")):
    controller = GetIncidentByIdController()
    return jsonable_encoder(controller.run(id_incident))
