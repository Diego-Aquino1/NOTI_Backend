from sqlalchemy.orm import Session
from models.inc_incidents import IncIncident # Asegúrate de tener este modelo definido

class IncidentMutations:
    def __init__(self, session: Session):
        self.db = session

    def get_by_id(self, id_incident: int) -> IncIncident | None:
        """Busca una incidencia por ID."""
        return self.db.query(IncIncident).filter(IncIncident.id == id_incident).first()
