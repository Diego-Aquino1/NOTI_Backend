# from math import radians, sin, cos, sqrt, atan2
# from typing import List
# from sqlalchemy.orm import Session
# from database import get_session
# from fastapi.encoders import jsonable_encoder
# from routers.geo_location.schemas.location_schemas import LocationCoordinateRequest
# from models.geo_locations import GeoLocation

# class FindIncidentController:
#     def __init__(self) -> None:
#         self.session: Session = get_session()

#     def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
#         """
#         Calcula la distancia de gran círculo entre dos puntos
#         en la Tierra (especificados en grados decimales) usando la fórmula de Haversine.
#         Devuelve la distancia en kilómetros.
#         """
#         # Radio de la Tierra en kilómetros
#         R = 6371.0

#         # Convierte latitud y longitud de grados a radianes
#         lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

#         # Diferencias en las coordenadas
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1

#         # Fórmula de Haversine
#         a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#         distance = R * c

#         return distance

#     def run(self, data: LocationCoordinateRequest) -> List[dict]:
#         """
#         Encuentra ubicaciones dentro de un radio de 5 km de las coordenadas dadas.
#         Devuelve una lista de diccionarios con id, latitud y longitud.
#         """
#         # Consulta todas las ubicaciones de la tabla geo_locations
#         locations = self.session.query(GeoLocation).all()

#         # Filtra ubicaciones dentro de un radio de 5 km usando la fórmula de Haversine
#         result = []
#         for location in locations:
#             distance = self.haversine(
#                 data.latitude, data.longitude, location.latitude, location.longitude
#             )
#             if distance <= 0.65:  # Radio de 650 metros (0.65 km)
#                 result.append({
#                     "id": location.id,
#                     "latitude": location.latitude,
#                     "longitude": location.longitude
#                 })

#         return result
from math import asin, radians, sin, cos, sqrt, atan2, degrees  # Importamos funciones matemáticas necesarias y degrees para convertir radianes a grados
from typing import List
from sqlalchemy.orm import Session
from database import get_session
from fastapi.encoders import jsonable_encoder
from routers.geo_location.schemas.location_schemas import LocationCoordinateRequest
from models.geo_locations import GeoLocation

class FindIncidentController:
    def __init__(self) -> None:
        self.session: Session = get_session()  # Inicializa la sesión de la base de datos

    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula la distancia en línea recta entre dos puntos en la Tierra
        especificados en grados decimales usando la fórmula de Haversine.
        Retorna la distancia en kilómetros.
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

    def get_bounding_box(self, latitude: float, longitude: float, radius_km: float = 5.0) -> tuple:
        """
        Calcula un cuadro delimitador alrededor de las coordenadas dadas para un radio especificado en km.
        Retorna (min_lat, max_lat, min_lon, max_lon).
        """
        # Radio de la Tierra en kilómetros
        R = 6371.0

        # Convierte el radio de kilómetros a radianes
        radius_rad = radius_km / R

        # Convierte latitud y longitud a radianes
        lat_rad = radians(latitude)
        lon_rad = radians(longitude)

        # Calcula los límites de la latitud
        min_lat = degrees(lat_rad - radius_rad)
        max_lat = degrees(lat_rad + radius_rad)

        # Calcula los límites de la longitud (ajusta según el rango de longitud dependiente de la latitud)
        delta_lon = asin(sin(radius_rad) / cos(lat_rad))
        min_lon = degrees(lon_rad - delta_lon)
        max_lon = degrees(lon_rad + delta_lon)

        return min_lat, max_lat, min_lon, max_lon

    def run(self, data: LocationCoordinateRequest) -> List[dict]:
        """
        Encuentra ubicaciones dentro de un radio de 5 km desde las coordenadas dadas.
        Retorna una lista de diccionarios con id, latitud y longitud.
        """
        # Calcula el cuadro delimitador para un radio de 5 km
        min_lat, max_lat, min_lon, max_lon = self.get_bounding_box(data.latitude, data.longitude, radius_km=5.0)

        # Consulta las ubicaciones dentro del cuadro delimitador
        locations = self.session.query(GeoLocation).filter(
            GeoLocation.latitude.between(min_lat, max_lat),
            GeoLocation.longitude.between(min_lon, max_lon)
        ).all()

        # Filtra las ubicaciones dentro de un radio de 5 km usando la fórmula de Haversine
        result = []
        for location in locations:
            distance = self.haversine(
                data.latitude, data.longitude, location.latitude, location.longitude
            )
            if distance <= 5.0:  # Radio de 5 km
                result.append({
                    "id": location.id,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })

        return result