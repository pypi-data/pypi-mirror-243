from pydantic import ValidationError as UnprocessableEntityError

class KnownError:
    pass

class UnauthenticatedError(Exception, KnownError):
    pass
    
class UnauthorizedError(Exception, KnownError):
    pass

def handle_error(exp: Exception, prefix: str, statusCode: int):
    error_dump = repr(exp)
    error_msg = f"{prefix}: {error_dump}"
    print(error_msg)
    return ({'error': error_msg}, statusCode)