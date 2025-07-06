from app.core.entities.candidate import Candidate
from app.core.repositories.candidate_repository import CandidateRepository
from app.core.exceptions import NotFoundError
from app.database.models import CandidateDB
from sqlalchemy.orm import Session
from typing import Optional

class SQLAlchemyCandidateRepository(CandidateRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: CandidateDB) -> Candidate:
        gender = Candidate.validate_gender_value(db_obj.gender)
        return Candidate(
            candidate_id=db_obj.candidate_id,
            name=db_obj.name,
            phone=db_obj.phone,
            email=db_obj.email,
            year_of_birth=db_obj.year_of_birth,
            gender=gender,
            education=db_obj.education,
            source=db_obj.source,
            expertise_id=db_obj.expertise_id,
            field_id=db_obj.field_id,
            area_id=db_obj.area_id,
            level_id=db_obj.level_id,
            headhunter_id=db_obj.headhunter_id,
            note=db_obj.note,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_candidate(self, candidate: Candidate) -> Candidate:
        new_candidate = CandidateDB(**candidate.to_dict())
        self.db_session.add(new_candidate)
        self.db_session.commit()
        self.db_session.refresh(new_candidate)
        return self._to_domain_entity(new_candidate)

    def get_candidate_by_id(self, candidate_id: int) -> Optional[Candidate]:
        if not candidate_id:
            raise ValueError("Candidate ID must be provided.")
        
        db_obj = self.db_session.get(CandidateDB, candidate_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_candidate(self, candidate: Candidate) -> Candidate:
        if not candidate.candidate_id:
            raise ValueError("Candidate ID must be provided for update.")
        
        db_obj = self.db_session.get(CandidateDB, candidate.candidate_id)
        if not db_obj:
            raise NotFoundError(entity="Candidate", identifier=candidate.candidate_id)
        
        for key, value in candidate.to_dict().items():
            setattr(db_obj, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_candidate(self, candidate_id: int) -> bool:
        if not candidate_id:
            raise ValueError("Candidate ID must be provided for deletion.")
        
        db_obj = self.db_session.get(CandidateDB, candidate_id)
        if not db_obj:
            raise NotFoundError(entity="Candidate", identifier=candidate_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True
