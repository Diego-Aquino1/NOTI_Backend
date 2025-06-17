from typing import List
from sqlalchemy.orm import Session
from database import get_session
from fastapi.encoders import jsonable_encoder
from routers.geo_location.schemas.location_schemas import LocationCoordinateRequest
from models.geo_locations import GeoLocation
from utilities.incident import haversine


class FindIncidentController:
    def __init__(self) -> None:
        self.session: Session = get_session()

    def run(self, data: LocationCoordinateRequest) -> List[dict]:
        """
        Encuentra ubicaciones dentro de un radio de 5 km de las coordenadas dadas.
        Devuelve una lista de diccionarios con id, latitud y longitud.
        """
        # Consulta todas las ubicaciones de la tabla geo_locations
        locations = self.session.query(GeoLocation).all()

        # Filtra ubicaciones dentro de un radio de 5 km usando la fórmula de Haversine
        result = []
        for location in locations:
            distance = haversine(
                data.latitude, data.longitude, location.latitude, location.longitude
            )
            if distance <= 0.65:  # Radio de 650 metros (0.65 km)
                result.append({
                    "id": location.id,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })

        return result