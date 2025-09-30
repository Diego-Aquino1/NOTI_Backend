# routers/geo_location/queries/incident_queries.py
from sqlmodel import Session
from shared.models.inc_incidents import IncIncident

class IncidentQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id_incident: int) -> IncIncident | None:
        return self.db.query(IncIncident).filter(IncIncident.id == id_incident).first()
