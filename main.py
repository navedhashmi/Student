from typing import Optional
from fastapi import FastAPI, Header, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from decorators import login_required
from utils import redirect, render
from schemas import NewUser
import models, auth
from utils import hash
from db_connection import engine, get_db, Se #Se = Session imported from db_connection


# Models Execution
models.Base.metadata.create_all(bind=engine)


#FastAPI app instance
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


#API Calls
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, "home.html")

@app.post("/register", response_class=HTMLResponse)
async def user_register(request: Request, form_data: NewUser = Depends(NewUser.register_form), db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    print(form_data)
    form_data.password = hash(form_data.password)
    new_user = models.User(**form_data.dict())
    print(new_user.password)
    try:
        db.add(new_user) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Username is already Registered")
    if hx_request:
        return render(request, "adduser.html")
    return render(request, "home.html")

@app.get("/adminpanel", response_class=HTMLResponse)
@login_required
def dashboard(request: Request):
    return render(request, "admin.html")

@app.get("/adduser", response_class=HTMLResponse)
@login_required
def add_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "adduser.html")

@app.get("/deleteuser", response_class=HTMLResponse)
@login_required
def delete_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "deleteuser.html")

@app.post("/getuser", response_class=HTMLResponse)
async def user_register(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    print(username)
    #try:
        #db.add(new_user) 
        #db.commit()
    #except:
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Username is already Registered")
    if hx_request is None:
        return HTTPException(status_code=404)
    return render(request, "deleteuser.html")


#Routers
app.include_router(auth.router)
