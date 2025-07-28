from sqlalchemy import Integer, VARCHAR, String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
import datetime

Base = declarative_base()

class CandidateDB(Base):
    __tablename__ = 'candidates'
    
    candidate_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    phone: Mapped[str] = mapped_column(VARCHAR(15), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    year_of_birth: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(VARCHAR(4), nullable=False)
    education: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(120), nullable=False)
    expertise_id: Mapped[int] = mapped_column(Integer, ForeignKey("expertises.expertise_id"), nullable=False)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.field_id"), nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey("areas.area_id"), nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, ForeignKey("levels.level_id"), nullable=False)
    headhunter_id: Mapped[int] = mapped_column(Integer, ForeignKey("headhunters.headhunter_id"), nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    expertise = relationship("ExpertiseDB", back_populates="candidates")
    field = relationship("FieldDB", back_populates="candidates")
    area = relationship("AreaDB", back_populates="candidates")
    level = relationship("LevelDB", back_populates="candidates")
    headhunter = relationship("HeadhunterDB", back_populates="candidates")
    nominees = relationship("NomineeDB", back_populates="candidate")

class ProjectDB(Base):
    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)
    budget_currency: Mapped[str] = mapped_column(VARCHAR(3), nullable=False)
    type: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    required_recruits: Mapped[int] = mapped_column(Integer, nullable=False)
    recruited: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    expertise_id: Mapped[int] = mapped_column(Integer, ForeignKey("expertises.expertise_id"), nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey("areas.area_id"), nullable=False)
    level_id: Mapped[int] = mapped_column(Integer, ForeignKey("levels.level_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    customer = relationship("CustomerDB", back_populates="projects")
    expertise = relationship("ExpertiseDB", back_populates="projects")
    area = relationship("AreaDB", back_populates="projects")
    level = relationship("LevelDB", back_populates="projects")
    nominees = relationship("NomineeDB", back_populates="project")

class NomineeDB(Base):
    __tablename__ = 'nominees'

    nominee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    campaign: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    salary_expectation: Mapped[float] = mapped_column(Float, nullable=False)
    notice_period: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_id: Mapped[int] = mapped_column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.project_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    candidate = relationship("CandidateDB", back_populates="nominees")
    project = relationship("ProjectDB", back_populates="nominees")

class CustomerDB(Base):
    __tablename__ = 'customers'

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    field_id: Mapped[int] = mapped_column(Integer, ForeignKey("fields.field_id"), nullable=False)
    representative_name: Mapped[str] = mapped_column(String(40), nullable=False)
    representative_phone: Mapped[str] = mapped_column(VARCHAR(15), nullable=False)
    representative_email: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    representative_role: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    field = relationship("FieldDB", back_populates="customers")
    projects = relationship("ProjectDB", back_populates="customer")

class HeadhunterDB(Base):
    __tablename__ = 'headhunters'

    headhunter_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    phone: Mapped[str] = mapped_column(VARCHAR(15), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    address: Mapped[str | None] = mapped_column(String(120), nullable=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    role: Mapped[str] = mapped_column(String(40), nullable=False)
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey("areas.area_id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    area = relationship("AreaDB", back_populates="headhunters")
    candidates = relationship("CandidateDB", back_populates="headhunter")

class LevelDB(Base):
    __tablename__ = 'levels'

    level_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    candidates = relationship("CandidateDB", back_populates="level")
    projects = relationship("ProjectDB", back_populates="level")

class ExpertiseDB(Base):
    __tablename__ = 'expertises'

    expertise_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    candidates = relationship("CandidateDB", back_populates="expertise")
    projects = relationship("ProjectDB", back_populates="expertise")

class FieldDB(Base):
    __tablename__ = 'fields'

    field_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    candidates = relationship("CandidateDB", back_populates="field")
    customers = relationship("CustomerDB", back_populates="field")

class AreaDB(Base):
    __tablename__ = 'areas'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.datetime.now(datetime.timezone.utc), 
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # Relationships
    candidates = relationship("CandidateDB", back_populates="area")
    projects = relationship("ProjectDB", back_populates="area")
    headhunters = relationship("HeadhunterDB", back_populates="area")