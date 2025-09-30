from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from ..controllers.incident_controller import IncidentController

router = APIRouter()

@router.get("/")
def get_incidents(session: Session = Depends(get_db)):
    """Get all incidents"""
    controller = IncidentController(session)
    return jsonable_encoder(controller.get_all_incidents())

@router.get("/{incident_id}")
def get_incident_by_id(incident_id: int, session: Session = Depends(get_db)):
    """Get incident by ID"""
    controller = IncidentController(session)
    return jsonable_encoder(controller.get_incident_by_id(incident_id))

@router.get("/active/")
def get_active_incidents(session: Session = Depends(get_db)):
    """Get active incidents"""
    controller = IncidentController(session)
    return jsonable_encoder(controller.get_active_incidents())
