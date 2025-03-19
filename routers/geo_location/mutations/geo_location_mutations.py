from sqlalchemy.orm import Session
from models.geo_locations import GeoLocation

class GeoLocationMutations:
    def __init__(self, session: Session):
        self.db = session

    def create(self, new_location: GeoLocation):
        """Guarda una nueva ubicación en la base de datos."""
        new_location.name = new_location.name or "Nombre de prueba"
        self.db.add(new_location)
        self.db.commit()
        self.db.refresh(new_location)
        return new_location
