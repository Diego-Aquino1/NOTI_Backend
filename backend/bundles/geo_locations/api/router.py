from fastapi import Query, APIRouter, Depends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from ..controllers.find_location_controller import FindLocationController
from ..controllers.massive_find_locations_controller import MassiveFindLocationsController
from ..controllers.find_location_coordinate import FindLocationCoordinateController
from ..controllers.find_incident import FindIncidentController
from ..schemas.location_schemas import LocationRequest, LocationCoordinateRequest
from ..controllers.find_incident_for_id import GetIncidentByIdController

router = APIRouter()

@router.post("/find", status_code = 200)
def register(data: LocationRequest, session: Session = Depends(get_db)):
    controller = FindLocationController(session)
    return jsonable_encoder(controller.run(data))

@router.post("/massive_find", status_code = 200)
def register(data: list[LocationRequest], session: Session = Depends(get_db)):
    controller = MassiveFindLocationsController(session)
    return jsonable_encoder(controller.run(data))

@router.post("/find_by_coordinates", status_code = 200)
def find_by_coordinates(data: LocationCoordinateRequest, session: Session = Depends(get_db)):
    controller = FindLocationCoordinateController(session)
    return jsonable_encoder(controller.run(data))

@router.post("/find_incidents_by_coordinates", status_code = 200)
def find_incidents_by_coordinates(data: LocationCoordinateRequest, session: Session = Depends(get_db)):
    controller = FindIncidentController(session)
    return jsonable_encoder(controller.run(data))

# Se busca un id de incident(corte)
@router.get("/find_incident", status_code = 200)
def get_incident_by_id(id_incident: int = Query(..., description="ID del incidente"), session: Session = Depends(get_db)):
    controller = GetIncidentByIdController(session)
    return jsonable_encoder(controller.run(id_incident))
