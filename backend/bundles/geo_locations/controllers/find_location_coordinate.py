from datetime import datetime
from shared.database.connection import get_session
from geopy.geocoders import Nominatim
from backend.bundles.geo_locations.schemas.location_schemas import LocationCoordinateRequest
from backend.bundles.geo_locations.mutations.geo_location_mutations import GeoLocationMutations
from shared.models.geo_locations import GeoLocation

class FindLocationCoordinateController:
    def __init__(self) -> None:
        session = get_session()
        self.geolocator = Nominatim(user_agent="geo_location_app")
        self.mutation = GeoLocationMutations(session)

    def run(self, data: LocationCoordinateRequest):
        # Perform reverse geocoding with latitude and longitude
        location = self.geolocator.reverse((data.latitude, data.longitude), addressdetails=True)

        if location:
            details = location.raw.get("address", {})

            location_data = GeoLocation(
                name="Nombre de prueba",
                address=location.address,
                latitude=location.latitude,
                longitude=location.longitude,
                city=details.get("city") or details.get("town") or details.get("village"),
                region=details.get("state"),
                country=details.get("country"),
                postal_code=details.get("postcode"),
            )

            # Save to the database
            self.mutation.create(location_data)

            return location_data
        else:
            return {"error": "No se encontraron resultados"}