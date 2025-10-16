from cims.core.entities.field import Field
from cims.core.repositories.field_repository import FieldRepository
from cims.database.models import FieldDB
from sqlalchemy.orm import Session
from cims.core.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyFieldRepository(FieldRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: FieldDB) -> Field:
        return Field(
            field_id=db_obj.field_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_field(self, field: Field) -> Field:
        db_obj = FieldDB(**field.to_dict())
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)
    
    def get_fields_by_ids(self, field_ids: list[int]) -> list[Field]:
        if not field_ids:
            return []
        
        db_fields = self.db_session.query(FieldDB).filter(FieldDB.field_id.in_(field_ids)).all()
        return [self._to_domain_entity(field) for field in db_fields]

    def get_field_by_id(self, field_id: int) -> Optional[Field]:
        if not field_id:
            return None
        
        db_obj = self.db_session.get(FieldDB, field_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_field(self, field: Field) -> Field:
        if not field.field_id:
            raise ValueError("Field ID must be provided for update.")
        
        db_obj = self.db_session.get(FieldDB, field.field_id)
        if not db_obj:
            raise NotFoundError(entity="Field", identifier=field.field_id)
        
        for key, value in field.to_dict().items():
            setattr(db_obj, key, value)
            
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_field(self, field_id: int) -> bool:
        if not field_id:
            raise ValueError("Field ID must be provided for deletion.")
        
        db_obj = self.db_session.get(FieldDB, field_id)
        if not db_obj:
            raise NotFoundError(entity="Field", identifier=field_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True

    def get_field_id_by_name(self, field_name: str) -> Optional[int]:
        if not field_name:
            raise ValueError("Field name must be provided.")
        
        db_obj = self.db_session.query(FieldDB).filter(FieldDB.name == field_name).first()
        if not db_obj:
            return None
        return db_obj.field_id

    def get_all_fields(self, limit: int = 100, offset: int = 0) -> list[Field]:
        db_objs = self.db_session.query(FieldDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(db_obj) for db_obj in db_objs]

    def search_fields_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Field]:
        db_objs = self.db_session.query(FieldDB).filter(
            FieldDB.name.ilike(f"%{name_query}%")
        ).offset(offset).limit(limit).all()
        return [self._to_domain_entity(db_obj) for db_obj in db_objs]