# Mock Data Injection Guide

This guide explains how to inject mock data into your CIMS PostgreSQL database.

## Overview

The mock data injection script creates:
- **10 Headhunters** with realistic profiles and credentials
- **70 Candidates** with diverse backgrounds and skills
- **30 Nominees** (selected from the 70 candidates) for various projects
- **20 Customers** representing different companies
- **Supporting data** including areas, fields, expertises, levels, and projects

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Start the database:**
   ```bash
   docker-compose up postgres -d
   ```

2. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit .env file** with your preferred database credentials (or use the defaults)

4. **Run the injection script:**
   ```bash
   ./setup_and_inject.sh
   ```

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env`
   - Update database credentials in `.env`

3. **Ensure PostgreSQL is running** and accessible with your credentials

4. **Run the injection script:**
   ```bash
   python inject_mock_data.py
   ```

## What Gets Created

### Lookup Tables
- **Areas**: 10 geographical regions (North America, Europe, Asia Pacific, etc.)
- **Fields**: 12 industry sectors (Technology, Healthcare, Finance, etc.)
- **Expertises**: 15 skill areas (Software Development, Data Science, etc.)
- **Levels**: 9 seniority levels (Entry Level to C-Level)

### Main Data
- **Headhunters**: 10 recruiters with hashed passwords (default: "password123")
- **Customers**: 20 companies across different industries
- **Projects**: 20-60 projects (1-3 per customer) with realistic budgets and timelines
- **Candidates**: 70 individuals with complete profiles
- **Nominees**: 30 candidates nominated for specific projects

## Data Characteristics

### Realistic Fake Data
- Names, emails, and phone numbers generated using Faker library
- Realistic salary expectations, experience levels, and notice periods
- Diverse geographical distribution and industry representation
- Proper foreign key relationships maintained

### Password Security
- All headhunter passwords are hashed using bcrypt
- Default password is "password123" for all accounts

### Date Logic
- Projects have logical start/end dates
- Timestamps use UTC timezone
- Created/updated timestamps are properly set

## Script Features

### Safety Features
- **Data Clearing**: Safely removes existing data before injection
- **Transaction Safety**: Uses database transactions for data integrity
- **Error Handling**: Proper rollback on failures
- **Foreign Key Respect**: Deletes in correct order to avoid constraint violations

### Flexibility
- Easy to modify data quantities by changing the loops
- Configurable through environment variables
- Extensible for additional data types

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check your `.env` file configuration
   - Ensure PostgreSQL is running
   - Verify network connectivity to database

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're in the correct directory

3. **Permission Errors**
   - Make sure the database user has CREATE/INSERT/DELETE permissions
   - For the shell script: `chmod +x setup_and_inject.sh`

4. **Table Already Exists Errors**
   - The script handles this automatically by clearing existing data
   - If issues persist, manually drop tables and re-run

### Verification

After running the script, you can verify the data:

```sql
-- Check record counts
SELECT 'headhunters' as table_name, COUNT(*) as count FROM headhunters
UNION ALL
SELECT 'candidates', COUNT(*) FROM candidates
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'nominees', COUNT(*) FROM nominees
UNION ALL
SELECT 'projects', COUNT(*) FROM projects;

-- Check relationships
SELECT h.name as headhunter, COUNT(c.candidate_id) as candidates_managed
FROM headhunters h
LEFT JOIN candidates c ON h.headhunter_id = c.headhunter_id
GROUP BY h.headhunter_id, h.name
ORDER BY candidates_managed DESC;
```

## Customization

To modify the data generation:

1. **Change quantities**: Edit the range values in the respective functions
2. **Add new fields**: Extend the data arrays (e.g., `areas_data`, `fields_data`)
3. **Modify relationships**: Adjust the foreign key assignments
4. **Custom data**: Replace Faker calls with your specific data

## Security Notes

- Default passwords are for development only
- Change default passwords before production use
- Environment variables should never be committed to version control
- Use strong, unique passwords for production databases
