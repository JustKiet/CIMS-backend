from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import Authenticator
from app.core.repositories.headhunter_repository import HeadhunterRepository
from app.usecases.authentication import HeadhunterAuthenticationUsecase, NotFoundError, InvalidCredentialsError
from app.schemas.requests.headhunter_create import HeadhunterCreate
from app.schemas.responses.headhunter_response import HeadhunterResponse
from app.schemas.responses.token import Token
from app.config import CLogger
from app.deps import get_headhunter_repository, get_authenticator
import traceback

logger = CLogger(__name__).get_logger()

logger.info("Initializing authentication router")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register")
async def _(
    payload: HeadhunterCreate,
    authenticator: Authenticator = Depends(get_authenticator),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
) -> HeadhunterResponse:
    """
    Register a new headhunter and return their details.
    
    :param HeadhunterCreate payload: The payload containing headhunter details.
    :return: HeadhunterResponse: A response containing the created headhunter's details.
    :rtype: HeadhunterResponse
    :raises HTTPException: If headhunter creation fails unexpectedly.
    """
    try:
        usecase = HeadhunterAuthenticationUsecase(
            headhunter_repository=headhunter_repo,
            authenticator=authenticator
        )

        response = usecase.register(payload)

        return response
    except Exception as e:
        logger.error(f"Unexpected error during headhunter registration: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
async def _(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticator: Authenticator = Depends(get_authenticator),
    headhunter_repo: HeadhunterRepository = Depends(get_headhunter_repository)
) -> Token:
    """
    Authenticate a headhunter and return their details.
    
    :param OAuth2PasswordRequestForm form_data: OAuth2PasswordRequestForm containing the username and password.
    :return: Token: A Token object containing the access token and token type.
    :rtype: Token
    :raises HTTPException: If authentication fails or headhunter not found.
    """
    try:
        usecase = HeadhunterAuthenticationUsecase(
            headhunter_repository=headhunter_repo,
            authenticator=authenticator
        )

        token = usecase.authenticate(form_data.username, form_data.password)

        return token
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
    
@router.get("/me")
async def get_current_headhunter(
    authenticator: Authenticator = Depends(get_authenticator),
) -> HeadhunterResponse:
    """
    Get the current authenticated headhunter's details.
    
    :return: HeadhunterResponse: A response containing the current headhunter's details.
    :rtype: HeadhunterResponse
    :raises HTTPException: If headhunter not found or authentication fails.
    """
    try:
        headhunter = authenticator.get_current_user()

        if not headhunter.headhunter_id:
            raise HTTPException(status_code=404, detail="Headhunter not found")

        return HeadhunterResponse(
            headhunter_id=headhunter.headhunter_id,
            name=headhunter.name,
            phone=headhunter.phone,
            email=headhunter.email,
            area_id=headhunter.area_id,
            role=headhunter.role
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