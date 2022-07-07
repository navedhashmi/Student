from fastapi import Request, HTTPException
from functools import wraps
from oauth2 import verify_access_token

#This Decorator is used to check if the user is logged in or not by checking the session_id cookie


def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        session_token = request.cookies.get('session_id')
        user_session = verify_access_token(session_token)
        if user_session is None:
            raise HTTPException(status_code=400)
        return func(request, *args, **kwargs)
    return wrapper