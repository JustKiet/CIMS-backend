#!/bin/bash

# Setup and run mock data injection script

echo "Setting up environment and injecting mock data..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.in

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one with your database credentials."
    echo "Required variables:"
    echo "POSTGRES_HOST=localhost"
    echo "POSTGRES_PORT=5432"
    echo "POSTGRES_USER=your_user"
    echo "POSTGRES_PASSWORD=your_password"
    echo "POSTGRES_DB=your_database"
    echo "SECRET_KEY=your_secret_key"
    exit 1
fi

# Run the mock data injection
echo "Running mock data injection..."
python inject_mock_data.py

echo "Mock data injection completed!"
