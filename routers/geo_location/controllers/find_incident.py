from math import radians, sin, cos, sqrt, atan2
from typing import List
from sqlalchemy.orm import Session
from database import get_session
from fastapi.encoders import jsonable_encoder
from routers.geo_location.schemas.location_schemas import LocationCoordinateRequest
from models.geo_locations import GeoLocation

class FindIncidentController:
    def __init__(self) -> None:
        self.session: Session = get_session()

    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula la distancia de gran círculo entre dos puntos
        en la Tierra (especificados en grados decimales) usando la fórmula de Haversine.
        Devuelve la distancia en kilómetros.
        """
        # Radio de la Tierra en kilómetros
        R = 6371.0

        # Convierte latitud y longitud de grados a radianes
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Diferencias en las coordenadas
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Fórmula de Haversine
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance

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
            distance = self.haversine(
                data.latitude, data.longitude, location.latitude, location.longitude
            )
            if distance <= 0.65:  # Radio de 650 metros (0.65 km)
                result.append({
                    "id": location.id,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })

        return result