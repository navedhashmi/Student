from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Password Hashing
def hash(password: str):
    return pass_context.hash(password)

#Password Verification
def verify(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)

#Template Rendering
def render()

#Redirect Responses
#def redirect(path, cookies:dict={}):
    #response = RedirectResponse(path, status_code=302)



