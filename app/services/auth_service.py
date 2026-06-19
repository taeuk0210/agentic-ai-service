from app.schemas import VerifyUserRequest, VerifyUserResponse


class AuthService:
    def __init__(self):
        pass

    def verify_user(self, req: VerifyUserRequest) -> VerifyUserResponse:
        pass


auth_service = AuthService()
