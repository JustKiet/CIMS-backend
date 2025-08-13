#!/usr/bin/env python3
"""
CIMS Mock Data Setup

This script provides interactive setup and execution of mock data injection.
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("📋 Please copy .env.example to .env and configure your database settings:")
        print("   cp .env.example .env")
        return False
    
    # Check if faker is installed
    try:
        import faker # type: ignore[import]
        print("✅ Faker library is available")
    except ImportError:
        print("❌ Faker library not found")
        print("📦 Installing Faker...")
        subprocess.run([sys.executable, "-m", "pip", "install", "faker"], check=True)
        print("✅ Faker installed successfully")
    
    return True

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*50)
    print("🎯 CIMS MOCK DATA INJECTION")
    print("="*50)
    print("1. 👀 Preview mock data (no database needed)")
    print("2. 🗄️  Inject mock data into database")
    print("3. 📚 View documentation")
    print("4. ❌ Exit")
    print("="*50)

def preview_data():
    """Run the preview script"""
    try:
        subprocess.run([sys.executable, "preview_mock_data.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error running preview script")
    except FileNotFoundError:
        print("❌ preview_mock_data.py not found")

def inject_data():
    """Run the data injection script"""
    print("🚀 Starting mock data injection...")
    print("⚠️  This will clear existing data and inject new mock data.")
    
    confirm = input("Do you want to continue? (y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ Injection cancelled")
        return
    
    try:
        subprocess.run([sys.executable, "inject_mock_data.py"], check=True)
        print("✅ Mock data injection completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during injection: {e}")
    except FileNotFoundError:
        print("❌ inject_mock_data.py not found")

def show_docs():
    """Show documentation"""
    try:
        with open("MOCK_DATA_README.md", "r") as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        print("❌ MOCK_DATA_README.md not found")

def main():
    """Main interactive function"""
    print("🎉 Welcome to CIMS Mock Data Setup!")
    
    if not check_requirements():
        print("❌ Requirements not met. Please fix the issues above and try again.")
        return
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            preview_data()
        elif choice == '2':
            inject_data()
        elif choice == '3':
            show_docs()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
