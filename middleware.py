import oauth2
from fastapi import Depends
import db_connection
from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials,
)

class JWTCookieBackend(AuthenticationBackend):
    async def authenticate(self, request):
        session_id = request.cookies.get("session_id")
        if session_id is None:
            roles = ["unauthenticated"]
            return UnauthenticatedUser(), AuthCredentials(roles)
        user_data = oauth2.verify_admin_user(session_id)
        print(user_data)
        #if user_data is None:
        #    roles = ["user"]
        #    return UnauthenticatedUser(), AuthCredentials(roles)
        #user_id = user_data.get("user_id")
        roles = ['admin']
        return AuthCredentials(roles), SimpleUser(user_data)