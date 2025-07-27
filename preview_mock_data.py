#!/usr/bin/env python3
"""
Mock Data Preview Script

This script shows what data would be generated without actually connecting to the database.
Useful for previewing and testing the data generation logic.

Usage:
    python preview_mock_data.py
"""

import random
from faker import Faker
from typing import Any

# Initialize Faker
fake = Faker()

def preview_areas():
    areas_data = [
        "North America", "Europe", "Asia Pacific", "Latin America", 
        "Middle East", "Africa", "Southeast Asia", "Eastern Europe",
        "Central America", "Oceania"
    ]
    return areas_data

def preview_fields():
    fields_data = [
        "Technology", "Healthcare", "Finance", "Education", "Manufacturing",
        "Retail", "Consulting", "Media", "Real Estate", "Transportation",
        "Energy", "Telecommunications"
    ]
    return fields_data

def preview_expertises():
    expertises_data = [
        "Software Development", "Data Science", "Project Management", 
        "Digital Marketing", "Financial Analysis", "HR Management",
        "Sales", "Operations", "Quality Assurance", "DevOps",
        "UI/UX Design", "Business Analysis", "Cybersecurity",
        "Cloud Architecture", "Mobile Development"
    ]
    return expertises_data

def preview_levels():
    levels_data = [
        "Entry Level", "Junior", "Mid-Level", "Senior", 
        "Lead", "Principal", "Director", "VP", "C-Level"
    ]
    return levels_data

def preview_headhunters(count: int = 10):
    roles = ["Senior Recruiter", "Lead Headhunter", "Talent Acquisition Manager", 
             "Executive Recruiter", "Technical Recruiter"]
    
    headhunters: list[dict[str, Any]] = []
    for i in range(count):
        headhunter: dict[str, Any] = {
            "id": i + 1,
            "name": fake.name(),
            "phone": fake.phone_number()[:15],
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "role": random.choice(roles),
            "area": random.choice(preview_areas())
        }
        headhunters.append(headhunter)
    
    return headhunters

def preview_customers(count: int = 20):
    company_types = ["Corp", "Inc", "LLC", "Ltd", "Technologies", "Solutions", 
                    "Systems", "Group", "Enterprises", "Industries"]
    
    customers: list[dict[str, Any]] = []
    for i in range(count):
        company_name = f"{fake.company().split()[0]} {random.choice(company_types)}"
        customer: dict[str, Any] = {
            "id": i + 1,
            "name": company_name,
            "field": random.choice(preview_fields())
        }
        customers.append(customer)
    
    return customers

def preview_candidates(count: int = 70):
    genders = ["M", "F", "NB"]
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
    
    candidates: list[dict[str, Any]] = []
    for i in range(count):
        candidate: dict[str, Any] = {
            "id": i + 1,
            "name": fake.name(),
            "phone": fake.phone_number()[:15],
            "email": fake.email(),
            "year_of_birth": random.randint(1970, 2000),
            "gender": random.choice(genders),
            "education": random.choice(education_levels),
            "source": random.choice(sources),
            "expertise": random.choice(preview_expertises()),
            "field": random.choice(preview_fields()),
            "area": random.choice(preview_areas()),
            "level": random.choice(preview_levels()),
            "note": fake.text(max_nb_chars=100) if random.choice([True, False]) else None
        }
        candidates.append(candidate)
    
    return candidates

def main():
    print("="*60)
    print("MOCK DATA PREVIEW")
    print("="*60)
    
    print("\n📍 AREAS:")
    areas = preview_areas()
    for i, area in enumerate(areas, 1):
        print(f"  {i:2d}. {area}")
    
    print("\n🏢 FIELDS:")
    fields = preview_fields()
    for i, field in enumerate(fields, 1):
        print(f"  {i:2d}. {field}")
    
    print("\n🛠️  EXPERTISES:")
    expertises = preview_expertises()
    for i, expertise in enumerate(expertises, 1):
        print(f"  {i:2d}. {expertise}")
    
    print("\n📊 LEVELS:")
    levels = preview_levels()
    for i, level in enumerate(levels, 1):
        print(f"  {i:2d}. {level}")
    
    print("\n👥 SAMPLE HEADHUNTERS (showing first 3):")
    headhunters = preview_headhunters(10)
    for i, hh in enumerate(headhunters[:3], 1):
        print(f"  {i}. {hh['name']} ({hh['role']}) - {hh['email']} - {hh['area']}")
    print(f"  ... and {len(headhunters)-3} more")
    
    print("\n🏢 SAMPLE CUSTOMERS (showing first 5):")
    customers = preview_customers(20)
    for i, customer in enumerate(customers[:5], 1):
        print(f"  {i}. {customer['name']} - {customer['field']}")
    print(f"  ... and {len(customers)-5} more")
    
    print("\n👤 SAMPLE CANDIDATES (showing first 5):")
    candidates = preview_candidates(70)
    for i, candidate in enumerate(candidates[:5], 1):
        print(f"  {i}. {candidate['name']} ({candidate['gender']}, {2025-candidate['year_of_birth']} years old)")
        print(f"     📧 {candidate['email']} | 📞 {candidate['phone']}")
        print(f"     🎓 {candidate['education']} | 🏢 {candidate['field']} | 🛠️  {candidate['expertise']}")
        print(f"     📍 {candidate['area']} | 📊 {candidate['level']}")
        print(f"     📝 Source: {candidate['source']}")
        if candidate['note']:
            print(f"     💬 Note: {candidate['note'][:50]}...")
        print()
    print(f"  ... and {len(candidates)-5} more")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Areas: {len(areas)}")
    print(f"Fields: {len(fields)}")
    print(f"Expertises: {len(expertises)}")
    print(f"Levels: {len(levels)}")
    print(f"Headhunters: {len(headhunters)}")
    print(f"Customers: {len(customers)}")
    print(f"Candidates: {len(candidates)}")
    print(f"Nominees: 30 (will be selected from candidates)")
    print(f"Projects: ~{len(customers) * 1.5:.0f} (1-3 per customer)")
    print("="*60)
    print("✅ Ready to inject into database!")

if __name__ == "__main__":
    main()
