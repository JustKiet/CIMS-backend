from app.core.entities.headhunter import Headhunter
from app.core.repositories.headhunter_repository import HeadhunterRepository
from app.database.models import HeadhunterDB
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyHeadhunterRepository(HeadhunterRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain_entity(self, db_obj: HeadhunterDB) -> Headhunter:
        return Headhunter(
            headhunter_id=db_obj.headhunter_id,
            name=db_obj.name,
            phone=db_obj.phone,
            email=db_obj.email,
            hashed_password=db_obj.hashed_password,
            role=db_obj.role,
            area_id=db_obj.area_id,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_headhunter(self, headhunter: Headhunter) -> Headhunter:
        # Convert domain entity to database model format
        headhunter_dict = headhunter.to_dict()
        # Remove created_at and updated_at as they are handled by the database
        headhunter_dict.pop('created_at', None)
        headhunter_dict.pop('updated_at', None)
        
        db_obj = HeadhunterDB(**headhunter_dict)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def get_headhunter_by_id(self, headhunter_id: int) -> Optional[Headhunter]:
        if not headhunter_id:
            raise ValueError("Headhunter ID must be provided.")
        
        db_obj = self.session.get(HeadhunterDB, headhunter_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)
    
    def get_headhunter_by_email(self, email: str) -> Optional[Headhunter]:
        if not email:
            raise ValueError("Email must be provided.")
        
        db_obj = self.session.query(HeadhunterDB).filter(HeadhunterDB.email == email).first()
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_headhunter(self, headhunter: Headhunter) -> Headhunter:
        if not headhunter.headhunter_id:
            raise ValueError("Headhunter ID must be provided for update.")
        
        db_obj = self.session.get(HeadhunterDB, headhunter.headhunter_id)
        if not db_obj:
            raise NotFoundError(entity="Headhunter", identifier=headhunter.headhunter_id)
        
        # Convert domain entity to database model format
        headhunter_dict = headhunter.to_dict()
        # Remove fields that shouldn't be updated directly
        headhunter_dict.pop('headhunter_id', None)
        headhunter_dict.pop('created_at', None)
        headhunter_dict.pop('updated_at', None)
        
        for key, value in headhunter_dict.items():
            setattr(db_obj, key, value)
            
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_headhunter(self, headhunter_id: int) -> bool:
        if not headhunter_id:
            raise ValueError("Headhunter ID must be provided for deletion.")
        
        db_obj = self.session.get(HeadhunterDB, headhunter_id)
        if not db_obj:
            raise NotFoundError(entity="Headhunter", identifier=headhunter_id)
        
        self.session.delete(db_obj)
        self.session.commit()
        return True