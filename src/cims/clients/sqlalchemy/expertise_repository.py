from cims.core.entities.expertise import Expertise
from cims.core.repositories.expertise_repository import ExpertiseRepository
from cims.database.models import ExpertiseDB
from sqlalchemy.orm import Session
from cims.core.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyExpertiseRepository(ExpertiseRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: ExpertiseDB) -> Expertise:
        return Expertise(
            expertise_id=db_obj.expertise_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_expertise(self, expertise: Expertise) -> Expertise:
        db_obj = ExpertiseDB(**expertise.to_dict())
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)
    
    def get_expertises_by_ids(self, expertise_ids: list[int]) -> list[Expertise]:
        if not expertise_ids:
            return []
        
        db_expertises = self.db_session.query(ExpertiseDB).filter(ExpertiseDB.expertise_id.in_(expertise_ids)).all()
        return [self._to_domain_entity(expertise) for expertise in db_expertises]

    def get_expertise_by_id(self, expertise_id: int) -> Optional[Expertise]:
        if not expertise_id:
            return None

        db_obj = self.db_session.get(ExpertiseDB, expertise_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_expertise(self, expertise: Expertise) -> Expertise:
        if not expertise.expertise_id:
            raise ValueError("Expertise ID must be provided for update.")
        
        db_obj = self.db_session.get(ExpertiseDB, expertise.expertise_id)
        if not db_obj:
            raise NotFoundError(entity="Expertise", identifier=expertise.expertise_id)
        
        for key, value in expertise.to_dict().items():
            setattr(db_obj, key, value)
            
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_expertise(self, expertise_id: int) -> bool:
        if not expertise_id:
            raise ValueError("Expertise ID must be provided for deletion.")
        
        expertise_db = self.db_session.get(ExpertiseDB, expertise_id)
        if not expertise_db:
            raise NotFoundError(entity="Expertise", identifier=expertise_id)
        
        self.db_session.delete(expertise_db)
        self.db_session.commit()
        return True

    def get_all_expertises(self, limit: int = 100, offset: int = 0) -> list[Expertise]:
        db_expertises = self.db_session.query(ExpertiseDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(expertise) for expertise in db_expertises]

    def get_expertise_id_by_name(self, expertise_name: str) -> Optional[int]:
        if not expertise_name:
            raise ValueError("Expertise name must be provided.")
        
        db_obj = self.db_session.query(ExpertiseDB).filter(ExpertiseDB.name == expertise_name).first()
        return db_obj.expertise_id if db_obj else None

    def search_expertises_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Expertise]:
        db_expertises = (
            self.db_session.query(ExpertiseDB)
            .filter(ExpertiseDB.name.ilike(f"%{name_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(expertise) for expertise in db_expertises]