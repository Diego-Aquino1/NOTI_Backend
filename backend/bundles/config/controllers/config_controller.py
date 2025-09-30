from sqlmodel import Session, select
from shared.models.res_config import ResConfig
from typing import List, Optional

class ConfigController:
    def __init__(self, session: Session):
        self.session = session

    def get_all_configs(self) -> List[ResConfig]:
        """Get all configurations"""
        statement = select(ResConfig)
        configs = self.session.exec(statement).all()
        return configs

    def get_config_by_key(self, config_key: str) -> Optional[ResConfig]:
        """Get configuration by key"""
        statement = select(ResConfig).where(ResConfig.key == config_key)
        config = self.session.exec(statement).first()
        return config
