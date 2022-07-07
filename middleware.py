import oauth2
from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials,
)

#Custom Backend to check if the use is admin or not

class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        session_id = request.cookies.get("session_id")
        if session_id is None or session_id == "": 
            roles = ["unauthenticated"]
            return UnauthenticatedUser(), AuthCredentials(roles)
        user_data = oauth2.verify_admin_user(session_id)
        if user_data is None:
            roles = ["user"]
            return UnauthenticatedUser(), AuthCredentials(roles)
        roles = ['admin']
        return AuthCredentials(roles), SimpleUser(user_data.id)