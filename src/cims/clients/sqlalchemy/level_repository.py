from cims.core.entities.level import Level
from cims.core.repositories.level_repository import LevelRepository
from cims.database.models import LevelDB
from sqlalchemy.orm import Session
from cims.core.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyLevelRepository(LevelRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: LevelDB) -> Level:
        return Level(
            level_id=db_obj.level_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_level(self, level: Level) -> Level:
        db_obj = LevelDB(**level.to_dict())
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)
    
    def get_levels_by_ids(self, level_ids: list[int]) -> list[Level]:
        if not level_ids:
            return []
        
        db_levels = self.db_session.query(LevelDB).filter(LevelDB.level_id.in_(level_ids)).all()
        return [self._to_domain_entity(level) for level in db_levels]

    def get_level_by_id(self, level_id: int) -> Optional[Level]:
        if not level_id:
            return None
        
        db_obj = self.db_session.get(LevelDB, level_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_level(self, level: Level) -> Level:
        if not level.level_id:
            raise ValueError("Level ID must be provided for update.")
        
        db_obj = self.db_session.get(LevelDB, level.level_id)
        if not db_obj:
            raise NotFoundError(entity="Level", identifier=level.level_id)
        
        for key, value in level.to_dict().items():
            setattr(db_obj, key, value)
            
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_level(self, level_id: int) -> bool:
        if not level_id:
            raise ValueError("Level ID must be provided for deletion.")
        
        level_db = self.db_session.get(LevelDB, level_id)
        if not level_db:
            raise NotFoundError(entity="Level", identifier=level_id)
        
        self.db_session.delete(level_db)
        self.db_session.commit()
        return True

    def get_all_levels(self, limit: int = 100, offset: int = 0) -> list[Level]:
        db_levels = self.db_session.query(LevelDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(level) for level in db_levels]

    def get_level_id_by_name(self, level_name: str) -> Optional[int]:
        if not level_name:
            raise ValueError("Level name must be provided.")
        
        db_obj = self.db_session.query(LevelDB).filter(LevelDB.name == level_name).first()
        return db_obj.level_id if db_obj else None

    def search_levels_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Level]:
        db_levels = (
            self.db_session.query(LevelDB)
            .filter(LevelDB.name.ilike(f"%{name_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(level) for level in db_levels]