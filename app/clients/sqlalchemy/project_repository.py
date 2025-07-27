from app.core.entities.project import Project
from app.core.repositories.project_repository import ProjectRepository
from app.core.exceptions import NotFoundError
from app.database.models import ProjectDB
from sqlalchemy.orm import Session
from typing import Optional

class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _to_domain_entity(self, db_obj: ProjectDB) -> Project:
        type = Project.validate_project_type(db_obj.type)
        status = Project.validate_project_status(db_obj.status)
        return Project(
            project_id=db_obj.project_id,
            name=db_obj.name,
            start_date=db_obj.start_date,
            end_date=db_obj.end_date,
            budget=db_obj.budget,
            budget_currency=db_obj.budget_currency,
            type=type,
            required_recruits=db_obj.required_recruits,
            recruited=db_obj.recruited,
            status=status,
            customer_id=db_obj.customer_id,
            expertise_id=db_obj.expertise_id,
            area_id=db_obj.area_id,
            level_id=db_obj.level_id,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_project(self, project: Project) -> Project:
        new_project = ProjectDB(**project.to_dict())
        self.db_session.add(new_project)
        self.db_session.commit()
        self.db_session.refresh(new_project)
        return self._to_domain_entity(new_project)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        if not project_id:
            raise ValueError("Project ID must be provided.")
        
        db_obj = self.db_session.get(ProjectDB, project_id)
        if not db_obj:
            return None
        return self._to_domain_entity(db_obj)

    def update_project(self, project: Project) -> Project:
        if not project.project_id:
            raise ValueError("Project ID must be provided for update.")
        
        db_obj = self.db_session.get(ProjectDB, project.project_id)
        if not db_obj:
            raise NotFoundError(entity="Project", identifier=project.project_id)
        
        for key, value in project.to_dict().items():
            setattr(db_obj, key, value)

        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return self._to_domain_entity(db_obj)

    def delete_project(self, project_id: int) -> bool:
        if not project_id:
            raise ValueError("Project ID must be provided for deletion.")
        
        db_obj = self.db_session.get(ProjectDB, project_id)
        if not db_obj:
            raise NotFoundError(entity="Project", identifier=project_id)

        self.db_session.delete(db_obj)
        self.db_session.commit()
        return True

    def get_all_projects(self, limit: int = 100, offset: int = 0) -> list[Project]:
        db_projects = self.db_session.query(ProjectDB).offset(offset).limit(limit).all()
        return [self._to_domain_entity(project) for project in db_projects]

    def search_projects_by_name(self, name_query: str, limit: int = 100, offset: int = 0) -> list[Project]:
        db_projects = (
            self.db_session.query(ProjectDB)
            .filter(ProjectDB.name.ilike(f"%{name_query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(project) for project in db_projects]