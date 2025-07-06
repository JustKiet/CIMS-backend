from app.core.entities.field import Field
from app.core.repositories.field_repository import FieldRepository
from app.database.models import FieldDB
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyFieldRepository(FieldRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain_entity(self, db_obj: FieldDB) -> Field:
        return Field(
            field_id=db_obj.field_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_field(self, field: Field) -> Field:
        db_obj = FieldDB(**field.to_dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def get_field_by_id(self, field_id: int) -> Optional[Field]:
        if not field_id:
            raise ValueError("Field ID must be provided.")
        
        db_obj = self.session.get(FieldDB, field_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_field(self, field: Field) -> Field:
        if not field.field_id:
            raise ValueError("Field ID must be provided for update.")
        
        db_obj = self.session.get(FieldDB, field.field_id)
        if not db_obj:
            raise NotFoundError(entity="Field", identifier=field.field_id)
        
        for key, value in field.to_dict().items():
            setattr(db_obj, key, value)
            
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_field(self, field_id: int) -> bool:
        if not field_id:
            raise ValueError("Field ID must be provided for deletion.")
        
        field_db = self.session.query(FieldDB).filter_by(id=field_id).first()
        if not field_db:
            raise NotFoundError(entity="Field", identifier=field_id)
        
        self.session.delete(field_db)
        self.session.commit()
        return True