from sqlmodel import Session, select
from shared.models.res_profiles import ResProfile
from typing import List, Optional

class ProfileController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_profiles(self) -> List[ResProfile]:
        """Get all profiles"""
        statement = select(ResProfile)
        profiles = self.session.exec(statement).all()
        return profiles

    def get_profile_by_id(self, profile_id: int) -> Optional[ResProfile]:
        """Get profile by ID"""
        statement = select(ResProfile).where(ResProfile.id == profile_id)
        profile = self.session.exec(statement).first()
        return profile
