from sqlmodel import Session, select
from shared.models.not_notification import NotNotification
from typing import List

class NotificationController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_notifications(self) -> List[NotNotification]:
        """Get all notifications"""
        statement = select(NotNotification)
        notifications = self.session.exec(statement).all()
        return notifications

    def get_user_notifications(self, user_id: int) -> List[NotNotification]:
        """Get notifications for a specific user"""
        statement = select(NotNotification).where(NotNotification.user_id == user_id)
        notifications = self.session.exec(statement).all()
        return notifications
