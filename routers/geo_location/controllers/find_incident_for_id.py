

from database import get_session
from routers.geo_location.mutations.incident_mutations import IncidentMutations
from models.inc_incidents import IncIncident 
from datetime import datetime

class GetIncidentByIdController:
    def __init__(self) -> None:
        session = get_session()
        self.mutation = IncidentMutations(session)

    def run(self, id_incident: int):
        incident: IncIncident = self.mutation.get_by_id(id_incident)

        if not incident:
            return {"error": f"No se encontró la incidencia con ID {id_incident}"}

        return {
            #"title": incident.title,
            #"start_time": incident.start_time.isoformat() if incident.start_time else None,
            "start_time": incident.start_time.isoformat() if isinstance(incident.start_time, datetime) else incident.start_time,
            #"end_time": incident.end_time.isoformat() if incident.end_time else None,
            "end_time": incident.end_time.isoformat() if isinstance(incident.end_time, datetime) else incident.end_time,
            "description": incident.description,
            "motivo": incident.type_id,
            "suspendido": incident.suspendido,
            "url": incident.url,
        }
