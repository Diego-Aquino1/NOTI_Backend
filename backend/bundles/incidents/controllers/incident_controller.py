from sqlmodel import Session, select
from shared.models.inc_incidents import IncIncident
from typing import List, Optional

class IncidentController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_incidents(self) -> List[IncIncident]:
        """Get all incidents"""
        statement = select(IncIncident)
        incidents = self.session.exec(statement).all()
        return incidents

    def get_incident_by_id(self, incident_id: int) -> Optional[IncIncident]:
        """Get incident by ID"""
        statement = select(IncIncident).where(IncIncident.id == incident_id)
        incident = self.session.exec(statement).first()
        return incident

    def get_active_incidents(self) -> List[IncIncident]:
        """Get active incidents (not suspended)"""
        statement = select(IncIncident).where(IncIncident.suspendido == False)
        incidents = self.session.exec(statement).all()
        return incidents
