from database import get_session
from routers.geo_location.mutations.incident_mutations import IncidentMutations
from routers.geo_location.queries.incident_queries import IncidentQueries
from models.inc_incidents import IncIncident, IncIncidentAddress
from datetime import datetime

class GetIncidentByIdController:
    def __init__(self) -> None:
        session = get_session()
        self.query = IncidentQueries(session)

    def run(self, id_incident: int):
        incident: IncIncident = self.query.get_by_id(id_incident)

        if not incident:
            return {"error": f"No se encontró la incidencia con ID {id_incident}"}

        incident_data = IncIncident(
            #"title": incident.title,
            id = incident.id,
            start_time = incident.start_time.isoformat() if isinstance(incident.start_time, datetime) else incident.start_time,
            end_time = incident.end_time.isoformat() if isinstance(incident.end_time, datetime) else incident.end_time,
            description = incident.description,
            type_id = incident.type_id,
            suspendido = incident.suspendido,
            url = incident.url,
            addresses = [ IncIncidentAddress(
                    id = address.id,
                    incident_id=address.incident_id,
                    location_id=address.location_id,
                    location = address.location,
                    created_at = address.created_at.isoformat()
                )
                for address in incident.addresses
            ]
        )
        return incident_data
