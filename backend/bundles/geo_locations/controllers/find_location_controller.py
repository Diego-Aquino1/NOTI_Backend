from datetime import datetime
from sqlmodel import Session
from geopy.geocoders import Nominatim

from backend.bundles.geo_locations.schemas.location_schemas import LocationRequest
from backend.bundles.geo_locations.mutations.geo_location_mutations import GeoLocationMutations
from shared.models.geo_locations import GeoLocation


# from shared.utils.auth import ApiAuth

class FindLocationController:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.geolocator = Nominatim(user_agent="geo_location_app")
        self.mutation = GeoLocationMutations(session)

    def run(self, data: LocationRequest):
        location = self.geolocator.geocode(data.address, addressdetails=True)

        if location:
            details = location.raw.get("address", {})

            location_data = GeoLocation(
                name = "Nombre de prueba",
                address = location.address,
                latitude = location.latitude,
                longitude = location.longitude,
                city = details.get("city") or details.get("town") or details.get("village"),
                region = details.get("state"),
                country = details.get("country"),
                postal_code = details.get("postcode"),
            )

            # Guardar en la base de datos
            self.mutation.create(location_data)

            return location_data
        else:
            return {"error": "No se encontraron resultados"}