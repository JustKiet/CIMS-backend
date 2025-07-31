from cims.core.entities.candidate import Candidate
from cims.core.repositories.candidate_repository import CandidateRepository
from cims.core.exceptions import NotFoundError
from cims.database.models import CandidateDB, ExpertiseDB, FieldDB, LevelDB, AreaDB, HeadhunterDB
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
    
    def count_all_candidates(self) -> int:
        return self.db_session.query(CandidateDB).count()
    
    def get_all_candidates(self, limit: int = 100, offset: int = 0) -> list[Candidate]:
        db_candidates = self.db_session.query(CandidateDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(candidate) for candidate in db_candidates]

    def get_candidate_id_by_name(self, candidate_name: str) -> Optional[int]:
        db_obj = self.db_session.query(CandidateDB).filter(CandidateDB.name == candidate_name).first()
        return db_obj.candidate_id if db_obj else None

    def search_candidates_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Candidate]:
        db_candidates = (
            self.db_session.query(CandidateDB)
            .filter(CandidateDB.name.ilike(f"%{name_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(candidate) for candidate in db_candidates]
    
    def search_candidates_with_filters(
        self,
        name: Optional[str] = None,
        expertise_id: Optional[int] = None,
        field_id: Optional[int] = None,
        area_id: Optional[int] = None,
        level_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Candidate]:
        query = self.db_session.query(CandidateDB)
        
        if name:
            query = query.filter(CandidateDB.name.ilike(f"%{name}%"))
        if expertise_id:
            query = query.filter(CandidateDB.expertise_id == expertise_id)
        if field_id:
            query = query.filter(CandidateDB.field_id == field_id)
        if area_id:
            query = query.filter(CandidateDB.area_id == area_id)
        if level_id:
            query = query.filter(CandidateDB.level_id == level_id)

        db_candidates = query.offset(offset).limit(limit).all()
        return [self._to_domain_entity(candidate) for candidate in db_candidates]
    
    def count_candidates_with_filters(
        self,
        name: Optional[str] = None,
        expertise_id: Optional[int] = None,
        field_id: Optional[int] = None,
        area_id: Optional[int] = None,
        level_id: Optional[int] = None,
    ) -> int:
        query = self.db_session.query(CandidateDB)
        
        if name:
            query = query.filter(CandidateDB.name.ilike(f"%{name}%"))
        if expertise_id:
            query = query.filter(CandidateDB.expertise_id == expertise_id)
        if field_id:
            query = query.filter(CandidateDB.field_id == field_id)
        if area_id:
            query = query.filter(CandidateDB.area_id == area_id)
        if level_id:
            query = query.filter(CandidateDB.level_id == level_id)

        return query.count()
    
    def get_candidates_by_ids(self, candidate_ids: list[int]) -> list[Candidate]:
        if not candidate_ids:
            return []
        
        db_candidates = self.db_session.query(CandidateDB).filter(CandidateDB.candidate_id.in_(candidate_ids)).all()
        return [self._to_domain_entity(candidate) for candidate in db_candidates]

    def get_candidate_by_id(self, candidate_id: int) -> Optional[Candidate]:
        if not candidate_id:
            return None

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
