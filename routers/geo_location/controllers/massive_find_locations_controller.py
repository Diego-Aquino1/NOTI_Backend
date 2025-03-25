from datetime import datetime
from database import get_session

from geopy.geocoders import Nominatim

from routers.geo_location.schemas.location_schemas import LocationRequest
from routers.geo_location.mutations.geo_location_mutations import GeoLocationMutations

from models.geo_locations import GeoLocation

# from utilities.auth import ApiAuth

class MassiveFindLocationsController:
    def __init__(self) -> None:
        session = get_session()
        self.geolocator = Nominatim(user_agent="geo_location_app")
        self.mutation = GeoLocationMutations(session)

    def run(self, data: list[LocationRequest]):
        results = []

        for location_data in data:
            location = self.geolocator.geocode(location_data.address, addressdetails=True)

            if location:
                details = location.raw.get("address", {})

                location_entry = GeoLocation(
                    name = "Nombre de prueba",
                    address = location.address,
                    latitude = location.latitude,
                    longitude = location.longitude,
                    city = details.get("city") or details.get("town") or details.get("village"),
                    region = details.get("state"),
                    country = details.get("country"),
                    postal_code = details.get("postcode"),
                )

                self.mutation.create(location_entry)
                results.append(location_entry)
            else:
                results.append({"error": f"No se encontró la ubicación para: {location_data.address}"})

        return results