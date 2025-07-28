"""
API Schemas for CIMS Backend.

This module provides comprehensive schemas for all API operations,
following production-grade standards with proper validation,
documentation, and response formatting.
"""

# Base schemas
from .base import (
    BaseResponse,
    DataResponse,
    ListResponse,
    PaginationMeta,
    ErrorResponse,
    PaginationParams,
    SearchParams,
)

# Authentication schemas
from .auth import (
    LoginRequest,
    Token,
    TokenData,
    LoginResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    ChangePasswordRequest,
)

# Entity schemas
from .candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateDetailResponse,
    CandidateListResponse,
)

from .headhunter import (
    HeadhunterCreate,
    HeadhunterUpdate,
    HeadhunterPasswordUpdate,
    HeadhunterResponse,
    HeadhunterDetailResponse,
    HeadhunterListResponse,
)

from .project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectListResponse,
)

from .customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerDetailResponse,
    CustomerListResponse,
)

from .area import (
    AreaCreate,
    AreaUpdate,
    AreaResponse,
    AreaDetailResponse,
    AreaListResponse,
)

from .level import (
    LevelCreate,
    LevelUpdate,
    LevelResponse,
    LevelDetailResponse,
    LevelListResponse,
)

from .expertise import (
    ExpertiseCreate,
    ExpertiseUpdate,
    ExpertiseResponse,
    ExpertiseDetailResponse,
    ExpertiseListResponse,
)

from .field import (
    FieldCreate,
    FieldUpdate,
    FieldResponse,
    FieldDetailResponse,
    FieldListResponse,
)

from .nominee import (
    NomineeCreate,
    NomineeUpdate,
    NomineeResponse,
    NomineeDetailResponse,
    NomineeListResponse,
)

__all__ = [
    # Base schemas
    "BaseResponse",
    "DataResponse",
    "ListResponse",
    "PaginationMeta",
    "ErrorResponse",
    "PaginationParams",
    "SearchParams",
    
    # Authentication schemas
    "LoginRequest",
    "Token",
    "TokenData",
    "LoginResponse",
    "RefreshTokenRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "ChangePasswordRequest",
    
    # Candidate schemas
    "CandidateCreate",
    "CandidateUpdate", 
    "CandidateResponse",
    "CandidateDetailResponse",
    "CandidateListResponse",
    
    # Headhunter schemas
    "HeadhunterCreate",
    "HeadhunterUpdate",
    "HeadhunterPasswordUpdate",
    "HeadhunterResponse",
    "HeadhunterDetailResponse",
    "HeadhunterListResponse",
    
    # Project schemas
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectDetailResponse",
    "ProjectListResponse",
    
    # Customer schemas
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "CustomerDetailResponse",
    "CustomerListResponse",
    
    # Area schemas
    "AreaCreate",
    "AreaUpdate",
    "AreaResponse",
    "AreaDetailResponse",
    "AreaListResponse",
    
    # Level schemas
    "LevelCreate",
    "LevelUpdate",
    "LevelResponse",
    "LevelDetailResponse",
    "LevelListResponse",
    
    # Expertise schemas
    "ExpertiseCreate",
    "ExpertiseUpdate",
    "ExpertiseResponse",
    "ExpertiseDetailResponse",
    "ExpertiseListResponse",
    
    # Field schemas
    "FieldCreate",
    "FieldUpdate",
    "FieldResponse",
    "FieldDetailResponse",
    "FieldListResponse",
    
    # Nominee schemas
    "NomineeCreate",
    "NomineeUpdate",
    "NomineeResponse",
    "NomineeDetailResponse",
    "NomineeListResponse",
]
