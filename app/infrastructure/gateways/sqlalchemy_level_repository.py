from app.domain.entities.level import Level
from app.domain.repositories.level_repository import LevelRepository
from app.infrastructure.database.models import LevelDB
from sqlalchemy.orm import Session
from app.domain.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyLevelRepository(LevelRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain_entity(self, db_obj: LevelDB) -> Level:
        return Level(
            level_id=db_obj.level_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_level(self, level: Level) -> Level:
        db_obj = LevelDB(**level.to_dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def get_level_by_id(self, level_id: int) -> Optional[Level]:
        if not level_id:
            raise ValueError("Level ID must be provided.")
        
        db_obj = self.session.get(LevelDB, level_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_level(self, level: Level) -> Level:
        if not level.level_id:
            raise ValueError("Level ID must be provided for update.")
        
        db_obj = self.session.get(LevelDB, level.level_id)
        if not db_obj:
            raise NotFoundError(entity="Level", identifier=level.level_id)
        
        for key, value in level.to_dict().items():
            setattr(db_obj, key, value)
            
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_level(self, level_id: int) -> bool:
        if not level_id:
            raise ValueError("Level ID must be provided for deletion.")
        
        level_db = self.session.query(LevelDB).filter_by(id=level_id).first()
        if not level_db:
            raise NotFoundError(entity="Level", identifier=level_id)
        
        self.session.delete(level_db)
        self.session.commit()
        return True