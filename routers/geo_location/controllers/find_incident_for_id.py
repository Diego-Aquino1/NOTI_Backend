

from database import get_session
from routers.geo_location.mutations.incident_mutations import IncidentMutations
from models.inc_incidents import IncIncident 

class GetIncidentByIdController:
    def __init__(self) -> None:
        session = get_session()
        self.mutation = IncidentMutations(session)

    def run(self, id_incident: int):
        incident: IncIncident = self.mutation.get_by_id(id_incident)

        if not incident:
            return {"error": f"No se encontró la incidencia con ID {id_incident}"}

        return {
            #"titulo": incident.titulo,
            "start_time": incident.start_time.isoformat() if incident.start_time else None,
            "end_time": incident.end_time.isoformat() if incident.end_time else None,
            "description": incident.description,
            "type_id": incident.type_id,
            "suspendido": incident.suspendido,
            "url": incident.url,
        }
