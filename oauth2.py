from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from config import get_settings
import db_connection, models


# Instance of Enviorment Variables
settings = get_settings()

#SECRET_KEY
SECERT_KEY = settings.secret_key
#Algorithm
ALGORITHM = settings.algorithm
#Expriation Time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
#Algorithm

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
        if id is None or username is None:
            return None
            # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return token_data

#verify_admin_user (This used in middleware)
def verify_admin_user(token: str, database_x = db_connection.SeassionLocal):
    try:
        payload = jwt.decode(token, SECERT_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        username: str = payload.get("username")
        if id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        #user = database_x.query(models.User).filter(models.User.username == username)
        database = database_x()
        user = database.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        if user.isAdmin == False:
            return None
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return token_data