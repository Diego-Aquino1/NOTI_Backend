from sqlalchemy.orm import Session
from shared.models.inc_incidents import IncIncident # Asegúrate de tener este modelo definido

class IncidentMutations:
    def __init__(self, session: Session):
        self.db = session

