from app.core.entities.area import Area
from app.core.repositories.area_repository import AreaRepository
from app.core.exceptions import NotFoundError
from app.database.models import AreaDB
from sqlalchemy.orm import Session
from typing import Optional

class SQLAlchemyAreaRepository(AreaRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: AreaDB) -> Area:
        return Area(
            area_id=db_obj.area_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_area(self, area: Area) -> Area:
        new_area = AreaDB(**area.to_dict())
        self.db_session.add(new_area)
        self.db_session.commit()
        self.db_session.refresh(new_area)
        return self._to_domain_entity(new_area)
    
    def get_all_areas(self, limit: int = 100, offset: int = 0) -> list[Area]:
        db_areas = self.db_session.query(AreaDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(area) for area in db_areas]

    def search_areas_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Area]:
        db_areas = (
            self.db_session.query(AreaDB)
            .filter(AreaDB.name.ilike(f"%{name_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(area) for area in db_areas]
    
    def get_area_id_by_name(self, area_name: str) -> Optional[int]:
        if not area_name:
            raise ValueError("Area name must be provided.")
        
        db_obj = self.db_session.query(AreaDB).filter(AreaDB.name == area_name).first()
        return db_obj.area_id if db_obj else None

    def get_area_by_id(self, area_id: int) -> Optional[Area]:
        if not area_id:
            raise ValueError("Area ID must be provided.")
        
        db_obj = self.db_session.get(AreaDB, area_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_area(self, area: Area) -> Area:
        if not area.area_id:
            raise ValueError("Area ID must be provided for update.")
        
        db_obj = self.db_session.get(AreaDB, area.area_id)
        if not db_obj:
            raise NotFoundError(entity="Area", identifier=area.area_id)
        
        for key, value in area.to_dict().items():
            setattr(db_obj, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_area(self, area_id: int) -> bool:
        if not area_id:
            raise ValueError("Area ID must be provided for deletion.")
        
        db_obj = self.db_session.get(AreaDB, area_id)
        if not db_obj:
            raise NotFoundError(entity="Area", identifier=area_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True