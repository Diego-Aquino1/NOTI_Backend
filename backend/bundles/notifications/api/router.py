from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from ..controllers.notification_controller import NotificationController

router = APIRouter()

@router.get("/")
def get_notifications(session: Session = Depends(get_db)):
    """Get all notifications"""
    controller = NotificationController(session)
    return jsonable_encoder(controller.get_all_notifications())

@router.get("/user/{user_id}")
def get_user_notifications(user_id: int, session: Session = Depends(get_db)):
    """Get notifications for a specific user"""
    controller = NotificationController(session)
    return jsonable_encoder(controller.get_user_notifications(user_id))
