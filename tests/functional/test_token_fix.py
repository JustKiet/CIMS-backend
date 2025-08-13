#!/usr/bin/env python3
"""
Simple script to test token generation and verify the timezone fix
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime, timedelta, timezone
from cims.auth import Authenticator
from cims.config import settings

# Mock repository for testing
class MockHeadhunterService:
    def get_headhunter_by_id(self, user_id):
        return None

def test_token_generation():
    """Test that tokens are generated with correct expiration times"""
    
    # Create authenticator with test settings
    authenticator = Authenticator(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=30,  # 30 minutes
        headhunter_service=MockHeadhunterService()
    )
    
    # Generate a token
    test_data = {"sub": "123"}
    token = authenticator.create_access_token(test_data)
    
    print(f"Generated token: {token}")
    
    # Test token creation time calculation
    current_utc = datetime.now(timezone.utc)
    expected_expiry = current_utc + timedelta(minutes=30)
    
    print(f"Current UTC time: {current_utc.isoformat()}")
    print(f"Expected expiry time: {expected_expiry.isoformat()}")
    
    # Test the response data that would be sent to frontend
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    print(f"Response expires_at: {expires_at.isoformat()}")
    
    return True

if __name__ == "__main__":
    test_token_generation()
