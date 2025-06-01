from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class NotNotification(SQLModel, table=True):
    __tablename__ = "not_notifications"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="res_users.id")
    incident_id: int = Field(foreign_key="inc_incidents.id")
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    seen: bool = Field(default=False)