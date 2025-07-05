from app.domain.entities.expertise import Expertise
from app.domain.repositories.expertise_repository import ExpertiseRepository
from app.infrastructure.database.models import ExpertiseDB
from sqlalchemy.orm import Session
from app.domain.exceptions import NotFoundError
from typing import Optional

class SQLAlchemyExpertiseRepository(ExpertiseRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain_entity(self, db_obj: ExpertiseDB) -> Expertise:
        return Expertise(
            expertise_id=db_obj.expertise_id,
            name=db_obj.name,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_expertise(self, expertise: Expertise) -> Expertise:
        db_obj = ExpertiseDB(**expertise.to_dict())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def get_expertise_by_id(self, expertise_id: int) -> Optional[Expertise]:
        if not expertise_id:
            raise ValueError("Expertise ID must be provided.")
        
        db_obj = self.session.get(ExpertiseDB, expertise_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_expertise(self, expertise: Expertise) -> Expertise:
        if not expertise.expertise_id:
            raise ValueError("Expertise ID must be provided for update.")
        
        db_obj = self.session.get(ExpertiseDB, expertise.expertise_id)
        if not db_obj:
            raise NotFoundError(entity="Expertise", identifier=expertise.expertise_id)
        
        for key, value in expertise.to_dict().items():
            setattr(db_obj, key, value)
            
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_expertise(self, expertise_id: int) -> bool:
        if not expertise_id:
            raise ValueError("Expertise ID must be provided for deletion.")
        
        expertise_db = self.session.get(ExpertiseDB, expertise_id)
        if not expertise_db:
            raise NotFoundError(entity="Expertise", identifier=expertise_id)
        
        self.session.delete(expertise_db)
        self.session.commit()
        return True