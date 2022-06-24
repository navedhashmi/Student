from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi.security.oauth2 import OAuth2PasswordBearer
from config import get_settings

# Instance of Enviorment Variables
settings = get_settings()

#SECRET_KEY
SECERT_KEY = settings.secret_key
#Algorithm
ALGORITHM = settings.algorithm
#Expriation Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
#Algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Create Access Token:
def create_access_token(data: dict):
    #We make a copy of data, So we don't change the original data.
    to_encode = data.copy()

    #We add a expire time to our encoded data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) 

    #This will create the JWT token with Payload(Which is out data=to_encode), Second is our secret key and lastly our Algo
    encoded_jwt = jwt.encode(to_encode, SECERT_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#Verify Access Token:
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        username: str = payload.get("username")
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)



# Ruff Code:
#error = {"ErrorNum": "401", "ErrorDetail": "UNAUTHORIZED"}
#headers = {"WWW-Authenticate": "Bearer"}
#return render(Request, "error.html", context=error, status_code=status.HTTP_401_UNAUTHORIZED, cookies=headers, error=True)
#return templates.TemplateResponse("error.html", {"request": Request, "ErrorNum": "401", "ErrorDetail": "UNAUTHORIZED"}, status_code=status.HTTP_401_UNAUTHORIZED)