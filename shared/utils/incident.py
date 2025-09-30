from math import radians, sin, cos, sqrt, atan2

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
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