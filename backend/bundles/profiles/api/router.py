from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from ..controllers.profile_controller import ProfileController

router = APIRouter()

@router.get("/")
def get_profiles(session: Session = Depends(get_db)):
    """Get all profiles"""
    controller = ProfileController(session)
    return jsonable_encoder(controller.get_all_profiles())

@router.get("/{profile_id}")
def get_profile_by_id(profile_id: int, session: Session = Depends(get_db)):
    """Get profile by ID"""
    controller = ProfileController(session)
    return jsonable_encoder(controller.get_profile_by_id(profile_id))
