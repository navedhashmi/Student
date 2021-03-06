from fastapi import APIRouter, Depends, status, HTTPException, Request, Header
import db_connection, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #Oauth2 built in credentials Schem

#Router Instance

router = APIRouter(tags=['Authentication']) 

#_________________________________________________________________________________________________________________________________________________________#

#Router Methods - User Login and redirect to Homepage
 
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: db_connection.Se = Depends(db_connection.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #This is the line where we use the oauth2.py file create access token function, we pass in just the User ID as data and get a access toekn with payload as ID
    # & expire time
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "username": user.username})
    token = {"session_id": access_token}
    return utils.redirect(path="/adminpanel", cookies=token)

#Logout Functionality
@router.get("/logout")
async def logout():
    token = {"session_id": "", "logout": "Logout Successfully"}
    return utils.redirect(path="/", cookies=token)