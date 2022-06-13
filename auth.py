from http import cookies
from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.responses import HTMLResponse
import db_connection, models, utils, oauth2
from fastapi.templating import Jinja2Templates
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #Oauth2 built in credentials Schema

router = APIRouter(tags=['Authentication']) 

templates = Jinja2Templates(directory="templates")

@router.post('/login/', response_class=HTMLResponse)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: db_connection.Se = Depends(db_connection.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #This is the line where we use the oauth2.py file create access token function, we pass in just the User ID as data and get a access toekn with payload as ID
    # & expire time
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "username": user.username})

    #return {'access_token': access_token, "token_type": "bearer"}
    context = {'request': request}
    return templates.TemplateResponse("home.html", context, cookies=access_token)