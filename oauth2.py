from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi.security.oauth2 import OAuth2PasswordBearer

#SECRET_KEY
SECERT_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#Algorithm
ALGORITHM = "HS256"
#Expriation Time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        username: str = payload.get("username")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)