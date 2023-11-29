
from .errors import UnauthenticatedError, UnauthorizedError
from pydantic import BaseModel, validator

class Authenticator(BaseModel):
    AUTH_TOKEN: str | None
    header_key: str = "Api-Token"

    @validator('AUTH_TOKEN')
    def auth_token_must_be_set(cls, token):
        if token is None:
            raise ValueError('must be set')
        return token

    def authenticate(self, request):
        token = request.headers.get(self.header_key)
        if not token:
            raise UnauthenticatedError()
        if token != self.AUTH_TOKEN:
            raise UnauthorizedError()
