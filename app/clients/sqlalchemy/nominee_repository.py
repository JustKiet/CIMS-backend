from app.core.entities.nominee import Nominee
from app.core.repositories.nominee_repository import NomineeRepository
from app.core.exceptions import NotFoundError
from app.database.models import NomineeDB
from sqlalchemy.orm import Session
from typing import Optional

class SQLAlchemyNomineeRepository(NomineeRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: NomineeDB) -> Nominee:
        status = Nominee.validate_nominee_status(db_obj.status)
        return Nominee(
            nominee_id=db_obj.nominee_id,
            campaign=db_obj.campaign,
            status=status,
            years_of_experience=db_obj.years_of_experience,
            salary_expectation=db_obj.salary_expectation,
            notice_period=db_obj.notice_period,
            candidate_id=db_obj.candidate_id,
            project_id=db_obj.project_id,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_nominee(self, nominee: Nominee) -> Nominee:
        new_nominee = NomineeDB(**nominee.to_dict())
        self.db_session.add(new_nominee)
        self.db_session.commit()
        self.db_session.refresh(new_nominee)
        return self._to_domain_entity(new_nominee)

    def get_nominee_by_id(self, nominee_id: int) -> Optional[Nominee]:
        if not nominee_id:
            raise ValueError("Nominee ID must be provided.")
        
        db_obj = self.db_session.get(NomineeDB, nominee_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_nominee(self, nominee: Nominee) -> Nominee:
        if not nominee.nominee_id:
            raise ValueError("Nominee ID must be provided for update.")
        
        db_obj = self.db_session.get(NomineeDB, nominee.nominee_id)
        if not db_obj:
            raise NotFoundError(entity="Nominee", identifier=nominee.nominee_id)
        
        for key, value in nominee.to_dict().items():
            setattr(db_obj, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_nominee(self, nominee_id: int) -> bool:
        if not nominee_id:
            raise ValueError("Nominee ID must be provided for deletion.")
        
        db_obj = self.db_session.get(NomineeDB, nominee_id)
        if not db_obj:
            raise NotFoundError(entity="Nominee", identifier=nominee_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True

    def get_all_nominees(self, limit: int = 100, offset: int = 0) -> list[Nominee]:
        db_nominees = self.db_session.query(NomineeDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(nominee) for nominee in db_nominees]

    def get_nominees_by_candidate_id(self, candidate_id: int, limit: int = 100, offset: int = 0) -> list[Nominee]:
        db_nominees = (
            self.db_session.query(NomineeDB)
            .filter(NomineeDB.candidate_id == candidate_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(nominee) for nominee in db_nominees]

    def get_nominees_by_project_id(self, project_id: int, limit: int = 100, offset: int = 0) -> list[Nominee]:
        db_nominees = (
            self.db_session.query(NomineeDB)
            .filter(NomineeDB.project_id == project_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(nominee) for nominee in db_nominees]

    def search_nominees_by_campaign(self, campaign_query: str, limit: int = 100, offset: int = 0) -> list[Nominee]:
        db_nominees = (
            self.db_session.query(NomineeDB)
            .filter(NomineeDB.campaign.ilike(f"%{campaign_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(nominee) for nominee in db_nominees]

    def search_nominees_by_status(self, status_query: str, limit: int = 100, offset: int = 0) -> list[Nominee]:
        db_nominees = (
            self.db_session.query(NomineeDB)
            .filter(NomineeDB.status == status_query)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(nominee) for nominee in db_nominees]