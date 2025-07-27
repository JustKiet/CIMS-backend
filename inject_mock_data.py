#!/usr/bin/env python3
"""
Mock Data Injection Script for CIMS Backend Database

This script creates and injects mock data into the PostgreSQL database:
- 10 Headhunters
- 70 Candidates (with 30 of them being nominees)
- 20 Customers
- Supporting data for areas, fields, expertises, levels, and projects

Usage:
    python inject_mock_data.py
"""

import os
import sys
import random
from typing import List
from faker import Faker
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.session import PostgresSessionFactory
from app.database.models import (
    CandidateDB, ProjectDB, NomineeDB, CustomerDB, 
    HeadhunterDB, LevelDB, ExpertiseDB, FieldDB, AreaDB
)
from app.config import settings
import bcrypt

# Initialize Faker
fake = Faker()

class MockDataInjector:
    def __init__(self):
        self.session_factory = PostgresSessionFactory(
            host="localhost",  # Use localhost for local development
            port=settings.POSTGRES_PORT,
            name=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD
        )
        
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def create_tables(self):
        """Create all database tables"""
        print("Creating database tables...")
        self.session_factory.create_tables()
        print("Tables created successfully!")

    def clear_existing_data(self, session: Session):
        """Clear existing data from all tables"""
        print("Clearing existing data...")
        
        # Delete in order to respect foreign key constraints
        session.query(NomineeDB).delete()
        session.query(CandidateDB).delete()
        session.query(ProjectDB).delete()
        session.query(CustomerDB).delete()
        session.query(HeadhunterDB).delete()
        session.query(LevelDB).delete()
        session.query(ExpertiseDB).delete()
        session.query(FieldDB).delete()
        session.query(AreaDB).delete()
        
        session.commit()
        print("Existing data cleared!")

    def create_areas(self, session: Session) -> List[AreaDB]:
        """Create area records"""
        print("Creating areas...")
        
        areas_data = [
            "North America", "Europe", "Asia Pacific", "Latin America", 
            "Middle East", "Africa", "Southeast Asia", "Eastern Europe",
            "Central America", "Oceania"
        ]
        
        areas: list[AreaDB] = []
        for area_name in areas_data:
            area = AreaDB(name=area_name)
            areas.append(area)
            session.add(area)
        
        session.commit()
        print(f"Created {len(areas)} areas")
        return areas

    def create_fields(self, session: Session) -> List[FieldDB]:
        """Create field records"""
        print("Creating fields...")
        
        fields_data = [
            "Technology", "Healthcare", "Finance", "Education", "Manufacturing",
            "Retail", "Consulting", "Media", "Real Estate", "Transportation",
            "Energy", "Telecommunications"
        ]
        
        fields: list[FieldDB] = []
        for field_name in fields_data:
            field = FieldDB(name=field_name)
            fields.append(field)
            session.add(field)
        
        session.commit()
        print(f"Created {len(fields)} fields")
        return fields

    def create_expertises(self, session: Session) -> List[ExpertiseDB]:
        """Create expertise records"""
        print("Creating expertises...")
        
        expertises_data = [
            "Software Development", "Data Science", "Project Management", 
            "Digital Marketing", "Financial Analysis", "HR Management",
            "Sales", "Operations", "Quality Assurance", "DevOps",
            "UI/UX Design", "Business Analysis", "Cybersecurity",
            "Cloud Architecture", "Mobile Development"
        ]
        
        expertises: list[ExpertiseDB] = []
        for expertise_name in expertises_data:
            expertise = ExpertiseDB(name=expertise_name)
            expertises.append(expertise)
            session.add(expertise)
        
        session.commit()
        print(f"Created {len(expertises)} expertises")
        return expertises

    def create_levels(self, session: Session) -> List[LevelDB]:
        """Create level records"""
        print("Creating levels...")
        
        levels_data = [
            "Entry Level", "Junior", "Mid-Level", "Senior", 
            "Lead", "Principal", "Director", "VP", "C-Level"
        ]
        
        levels: list[LevelDB] = []
        for level_name in levels_data:
            level = LevelDB(name=level_name)
            levels.append(level)
            session.add(level)
        
        session.commit()
        print(f"Created {len(levels)} levels")
        return levels

    def create_headhunters(self, session: Session, areas: List[AreaDB]) -> List[HeadhunterDB]:
        """Create 10 headhunter records"""
        print("Creating headhunters...")
        
        roles = ["Senior Recruiter", "Lead Headhunter", "Talent Acquisition Manager", 
                "Executive Recruiter", "Technical Recruiter"]
        
        headhunters: list[HeadhunterDB] = []
        for _ in range(10):
            headhunter = HeadhunterDB(
                name=fake.name(),
                phone=fake.phone_number()[:15],
                email=fake.email(),
                address=fake.address(),
                hashed_password=self.hash_password("password123"),  # Default password
                role=random.choice(roles),
                area_id=random.choice(areas).area_id
            )
            headhunters.append(headhunter)
            session.add(headhunter)
        
        session.commit()
        print(f"Created {len(headhunters)} headhunters")
        return headhunters

    def create_customers(self, session: Session, fields: List[FieldDB]) -> List[CustomerDB]:
        """Create 20 customer records"""
        print("Creating customers...")
        
        company_types = ["Corp", "Inc", "LLC", "Ltd", "Technologies", "Solutions", 
                        "Systems", "Group", "Enterprises", "Industries"]
        
        customers: list[CustomerDB] = []
        for _ in range(20):
            company_name = f"{fake.company().split()[0]} {random.choice(company_types)}"
            customer = CustomerDB(
                name=company_name,
                field_id=random.choice(fields).field_id,
                representative_name=fake.name(),
                representative_phone=fake.phone_number()[:15],
                representative_email=fake.email(),
                representative_role=random.choice(["Manager", "Director", "VP", "Executive"]),
            )
            customers.append(customer)
            session.add(customer)
        
        session.commit()
        print(f"Created {len(customers)} customers")
        return customers

    def create_projects(self, session: Session, customers: List[CustomerDB], 
                       expertises: List[ExpertiseDB], areas: List[AreaDB], 
                       levels: List[LevelDB]) -> List[ProjectDB]:
        """Create project records"""
        print("Creating projects...")
        
        project_types = ["CODINH", "THOIVU"]
        statuses = ["TIMKIEMUNGVIEN", "UNGVIENPHONGVAN", "UNGVIENTHUVIEC", "TAMNGUNG", "HUY", "HOANTHANH"]
        currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]
        
        projects: list[ProjectDB] = []
        for customer in customers:
            # Each customer gets 1-3 projects
            num_projects = random.randint(1, 3)
            for _ in range(num_projects):
                start_date = fake.date_between(start_date="-1y", end_date="today")
                end_date = fake.date_between(start_date=start_date, end_date="+6m")
                
                project = ProjectDB(
                    name=f"{fake.catch_phrase()} Project",
                    start_date=start_date,
                    end_date=end_date,
                    budget=round(random.uniform(50000, 500000), 2),
                    budget_currency=random.choice(currencies),
                    type=random.choice(project_types),
                    required_recruits=random.randint(1, 10),
                    recruited=random.randint(0, 10),
                    status=random.choice(statuses),
                    customer_id=customer.customer_id,
                    expertise_id=random.choice(expertises).expertise_id,
                    area_id=random.choice(areas).area_id,
                    level_id=random.choice(levels).level_id
                )
                projects.append(project)
                session.add(project)
        
        session.commit()
        print(f"Created {len(projects)} projects")
        return projects

    def create_candidates(self, session: Session, expertises: List[ExpertiseDB], 
                         fields: List[FieldDB], areas: List[AreaDB], 
                         levels: List[LevelDB], headhunters: List[HeadhunterDB]) -> List[CandidateDB]:
        """Create 70 candidate records"""
        print("Creating candidates...")
        
        genders = ["NAM", "NU", "KHAC"]
        education_levels = [
            "Bachelor's in Computer Science", "Master's in Business Administration",
            "Bachelor's in Engineering", "Master's in Data Science", 
            "PhD in Computer Science", "Bachelor's in Marketing",
            "Master's in Finance", "Bachelor's in Psychology",
            "Master's in Project Management", "Bachelor's in Economics"
        ]
        sources = [
            "LinkedIn", "Indeed", "Company Website", "Referral", 
            "Job Fair", "University Career Center", "Recruitment Agency",
            "Professional Network", "Social Media", "Direct Application"
        ]
        
        candidates: list[CandidateDB] = []
        for _ in range(70):
            candidate = CandidateDB(
                name=fake.name(),
                phone=fake.phone_number()[:15],
                email=fake.email(),
                year_of_birth=random.randint(1970, 2000),
                gender=random.choice(genders),
                education=random.choice(education_levels),
                source=random.choice(sources),
                expertise_id=random.choice(expertises).expertise_id,
                field_id=random.choice(fields).field_id,
                area_id=random.choice(areas).area_id,
                level_id=random.choice(levels).level_id,
                headhunter_id=random.choice(headhunters).headhunter_id,
                note=fake.text(max_nb_chars=200) if random.choice([True, False]) else None
            )
            candidates.append(candidate)
            session.add(candidate)
        
        session.commit()
        print(f"Created {len(candidates)} candidates")
        return candidates

    def create_nominees(self, session: Session, candidates: List[CandidateDB], 
                       projects: List[ProjectDB]) -> List[NomineeDB]:
        """Create 30 nominee records from existing candidates"""
        print("Creating nominees...")
        
        statuses = ["DECU", "PHONGVAN", "THUONGLUONG", "THUVIEC", "TUCHOI", "KYHOPDONG"]
        campaigns = [
            "Q1 Hiring Drive", "Tech Talent Search", "Senior Leadership Hunt",
            "Graduate Recruitment", "Expert Acquisition", "Rapid Hiring",
            "Strategic Placement", "Executive Search", "Skill-specific Hunt"
        ]
        
        # Select 30 random candidates to be nominees
        selected_candidates = random.sample(candidates, 30)
        
        nominees: list[NomineeDB] = []
        for candidate in selected_candidates:
            nominee = NomineeDB(
                campaign=random.choice(campaigns),
                status=random.choice(statuses),
                years_of_experience=random.randint(0, 20),
                salary_expectation=round(random.uniform(40000, 200000), 2),
                notice_period=random.randint(0, 90),  # days
                candidate_id=candidate.candidate_id,
                project_id=random.choice(projects).project_id
            )
            nominees.append(nominee)
            session.add(nominee)
        
        session.commit()
        print(f"Created {len(nominees)} nominees")
        return nominees

    def inject_all_data(self):
        """Main method to inject all mock data"""
        print("Starting mock data injection...")
        
        with self.session_factory.get_session() as session:
            try:
                # Clear existing data
                self.clear_existing_data(session)
                
                # Create lookup tables first
                areas = self.create_areas(session)
                fields = self.create_fields(session)
                expertises = self.create_expertises(session)
                levels = self.create_levels(session)
                
                # Create main entities
                headhunters = self.create_headhunters(session, areas)
                customers = self.create_customers(session, fields)
                projects = self.create_projects(session, customers, expertises, areas, levels)
                candidates = self.create_candidates(session, expertises, fields, areas, levels, headhunters)
                nominees = self.create_nominees(session, candidates, projects)
                
                print("\n" + "="*50)
                print("MOCK DATA INJECTION SUMMARY")
                print("="*50)
                print(f"Areas: {len(areas)}")
                print(f"Fields: {len(fields)}")
                print(f"Expertises: {len(expertises)}")
                print(f"Levels: {len(levels)}")
                print(f"Headhunters: {len(headhunters)}")
                print(f"Customers: {len(customers)}")
                print(f"Projects: {len(projects)}")
                print(f"Candidates: {len(candidates)}")
                print(f"Nominees: {len(nominees)}")
                print("="*50)
                print("Mock data injection completed successfully!")
                
            except Exception as e:
                session.rollback()
                print(f"Error during data injection: {e}")
                raise


def main():
    """Main function to run the mock data injection"""
    try:
        injector = MockDataInjector()
        
        # Create tables if they don't exist
        injector.create_tables()
        
        # Inject mock data
        injector.inject_all_data()
        
    except Exception as e:
        print(f"Failed to inject mock data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
