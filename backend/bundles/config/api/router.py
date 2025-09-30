from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from ..controllers.config_controller import ConfigController

router = APIRouter()

@router.get("/")
def get_configs(session: Session = Depends(get_db)):
    """Get all configurations"""
    controller = ConfigController(session)
    return jsonable_encoder(controller.get_all_configs())

@router.get("/{config_key}")
def get_config_by_key(config_key: str, session: Session = Depends(get_db)):
    """Get configuration by key"""
    controller = ConfigController(session)
    return jsonable_encoder(controller.get_config_by_key(config_key))
