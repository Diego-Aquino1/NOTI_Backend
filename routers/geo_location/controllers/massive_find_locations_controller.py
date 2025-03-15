from datetime import datetime
from database import get_session

from geopy.geocoders import Nominatim

from routers.geo_location.schemas.location_schemas import LocationRequest


# from utilities.auth import ApiAuth

class MassiveFindLocationsController:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent="noti_app_geocodification")

    # def run(self, auth: ApiAuth):
    def run(self, data: list[LocationRequest]):
        results = []

        for location_data in data:
            location = self.geolocator.geocode(location_data.address, addressdetails=True)
            
            if location:
                details = location.raw.get("address", {})
                results.append({
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "city": details.get("city") or details.get("town") or details.get("village"),
                    "region": details.get("state"),
                    "country": details.get("country"),
                    "postal_code": details.get("postcode"),
                })
            else:
                results.append({"error": f"No se encontró la ubicación para: {location_data}"})

        return results