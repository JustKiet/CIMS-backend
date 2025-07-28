from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from cims.auth import Authenticator, oauth2_scheme
from cims.core.repositories.headhunter_repository import HeadhunterRepository
from cims.usecases.authentication import HeadhunterAuthenticationUsecase, NotFoundError, InvalidCredentialsError
from cims.schemas import (
    HeadhunterCreate,
    HeadhunterResponse,
    HeadhunterDetailResponse,
    LoginResponse,
    TokenData,
    ErrorResponse,
)
from cims.schemas.utils import entity_to_response_model
from cims.config import CLogger
from cims.deps import get_headhunter_repository, get_authenticator
import traceback
from datetime import datetime, timedelta

logger = CLogger(__name__).get_logger()

logger.info("Initializing authentication router")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"model": ErrorResponse, "description": "Headhunter not found"},
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        400: {"model": ErrorResponse, "description": "Invalid request data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)

@router.post("/register",
    response_model=HeadhunterDetailResponse,
    status_code=201,
    summary="Register new headhunter",
    description="Register a new headhunter and return their details"
)
async def register_headhunter(
    payload: HeadhunterCreate,
    authenticator: Authenticator = Depends(get_authenticator),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
) -> HeadhunterDetailResponse:
    """
    Register a new headhunter and return their details.
    
    :param HeadhunterCreate payload: The payload containing headhunter details.
    :return: HeadhunterDetailResponse: A response containing the created headhunter's details.
    :rtype: HeadhunterDetailResponse
    :raises HTTPException: If headhunter creation fails unexpectedly.
    """
    try:
        usecase = HeadhunterAuthenticationUsecase(
            headhunter_repository=headhunter_repo,
            authenticator=authenticator
        )

        headhunter = usecase.register(payload)
        headhunter_response = entity_to_response_model(headhunter, HeadhunterResponse)

        return HeadhunterDetailResponse(
            success=True,
            message="Headhunter registered successfully",
            data=headhunter_response
        )
    except Exception as e:
        logger.error(f"Unexpected error during headhunter registration: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login",
    response_model=LoginResponse,
    summary="Authenticate headhunter",
    description="Authenticate a headhunter and return access token with enhanced details"
)
async def login_headhunter(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticator: Authenticator = Depends(get_authenticator),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
) -> LoginResponse:
    """
    Authenticate a headhunter and return their details.
    
    :param OAuth2PasswordRequestForm form_data: OAuth2PasswordRequestForm containing the username and password.
    :return: LoginResponse: A response containing the access token with enhanced details.
    :rtype: LoginResponse
    :raises HTTPException: If authentication fails or headhunter not found.
    """
    try:
        usecase = HeadhunterAuthenticationUsecase(
            headhunter_repository=headhunter_repo,
            authenticator=authenticator
        )

        token = usecase.authenticate(form_data.username, form_data.password)
        
        # Create enhanced token data
        expires_at = datetime.now() + timedelta(minutes=30)  # Assuming 30 min expiry
        token_data = TokenData(
            access_token=token.access_token,
            token_type=token.token_type,
            expires_in=1800,  # 30 minutes in seconds
            expires_at=expires_at
        )

        return LoginResponse(
            success=True,
            message="Authentication successful",
            data=token_data
        )
    except NotFoundError as e:
        logger.error(f"Headhunter not found: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=404, detail=str(e))
    
    except InvalidCredentialsError as e:
        logger.error(f"Authentication failed for user {form_data.username}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=401, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/me",
    response_model=HeadhunterDetailResponse,
    summary="Get current headhunter",
    description="Get the current authenticated headhunter's details"
)
async def get_current_headhunter(
    authenticator: Authenticator = Depends(get_authenticator),
    token: str = Depends(oauth2_scheme)
) -> HeadhunterDetailResponse:
    """
    Get the current authenticated headhunter's details.
    
    :return: HeadhunterDetailResponse: A response containing the current headhunter's details.
    :rtype: HeadhunterDetailResponse
    :raises HTTPException: If headhunter not found or authentication fails.
    """
    try:
        headhunter = authenticator.get_current_user(token)

        if not headhunter.headhunter_id:
            raise HTTPException(status_code=404, detail="Headhunter not found")

        headhunter_response = entity_to_response_model(headhunter, HeadhunterResponse)

        return HeadhunterDetailResponse(
            success=True,
            message="Current headhunter retrieved successfully",
            data=headhunter_response
        )
    
    except HTTPException as e:
        logger.error(f"HTTPException occurred: {str(e.detail)}")
        logger.error(traceback.format_exc())
        raise e
    
    except NotFoundError as e:
        logger.error(f"Headhunter not found: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        print(f"Unexpected error while fetching current headhunter: {str(e)}")
        logger.error(f"Unexpected error while fetching current headhunter: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")