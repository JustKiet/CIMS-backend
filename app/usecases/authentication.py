from app.infrastructure.auth import Authenticator
from app.domain.repositories.headhunter_repository import HeadhunterRepository
from app.domain.exceptions import NotFoundError, InvalidCredentialsError, UnexpectedError
from app.schemas.requests.headhunter_create import HeadhunterCreate
from app.schemas.responses.token import Token
from app.schemas.responses.headhunter_out import HeadhunterOut
from app.domain.entities.headhunter import Headhunter
from app.infrastructure.config import CLogger

logger = CLogger(__name__).get_logger()

class HeadhunterAuthenticationUsecase:
    def __init__(self, headhunter_repository: HeadhunterRepository, authenticator: Authenticator):
        self.headhunter_repository = headhunter_repository
        self.authenticator = authenticator

    def register(self, payload: HeadhunterCreate) -> HeadhunterOut:
        """
        Register a new headhunter.

        :param HeadhunterCreate payload: The payload containing headhunter details.
        :return: A response containing the created headhunter's details.
        :rtype: HeadhunterOut
        :raises UnexpectedError: If the headhunter creation fails unexpectedly.
        """
        headhunter = Headhunter(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            hashed_password=self.authenticator.get_password_hash(payload.password),
            area_id=payload.area_id,
            role=payload.role,
        )

        headhunter = self.headhunter_repository.create_headhunter(headhunter)
        
        if not headhunter.headhunter_id:
            logger.error("Failed to create headhunter. No ID returned.")
            raise UnexpectedError("Failed to create headhunter. No ID returned.")
        
        return HeadhunterOut(
            headhunter_id=headhunter.headhunter_id,
            name=headhunter.name,
            phone=headhunter.phone,
            email=headhunter.email,
            area_id=headhunter.area_id,
            role=headhunter.role,
        )
    
    def authenticate(self, email: str, password: str) -> Token:
        """
        Authenticate a headhunter and return their details.

        :param str email: The email of the headhunter.
        :param str password: The password of the headhunter.
        :return: A Token object containing the access token and token type.
        :rtype: Token
        :raises NotFoundError: If the headhunter with the given email does not exist.
        :raises InvalidCredentialsError: If the provided password does not match the stored hashed password.
        """
        headhunter = self.headhunter_repository.get_headhunter_by_email(email)
        if not headhunter:
            logger.error(f"Headhunter with email '{email}' not found.")
            raise NotFoundError(entity="Headhunter", identifier=email)

        if not self.authenticator.verify_password(password, headhunter.hashed_password):
            logger.error("Invalid email or password provided.")
            raise InvalidCredentialsError("Invalid email or password")
        
        access_token = self.authenticator.create_access_token(
            data={"sub": headhunter.headhunter_id},
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )
