from typing import Optional
from fastapi import FastAPI, Header, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from decorators import login_required
from utils import redirect, render
from schemas import NewUser, UpdateUser
import models, auth
from utils import hash, userdata_list
from starlette.exceptions import HTTPException as HTTPStarException
from db_connection import engine, get_db, Se #Se = Session imported from db_connection

# Models Execution
models.Base.metadata.create_all(bind=engine)


#FastAPI app instance
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


#Exception-Handler
@app.exception_handler(HTTPStarException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "error.html"
    context = {"ErrorNum": status_code, "ErrorDetail": "Error"}
    return render(request, template_name, context, status_code=status_code)


#API Calls

#_________________________________________________________________________________________________________________________________________________________#

#####################___Homepage__#####################

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, "home.html")

#####################___Register | Add__#####################

@app.post("/register", response_class=HTMLResponse) # This Call used in Add User
async def user_register(request: Request, form_data: NewUser = Depends(NewUser.register_form), db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    form_data.password = hash(form_data.password)
    new_user = models.User(**form_data.dict())
    try:
        db.add(new_user) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Username is already Registered")
    if hx_request:
        return render(request, "adduser.html")
    return render(request, "home.html")

#API Calls : Require User Login
#_________________________________________________________________________________________________________________________________________________________#

#####################___AdminDashboard-Home__#####################

@app.get("/adminpanel", response_class=HTMLResponse)
@login_required
def admin_home(request: Request):
    return render(request, "admin.html")

#####################___AdminDashboard-NavBar-Buttons__#####################
# Dashboard WIP
@app.get("/admindashboard", response_class=HTMLResponse)
@login_required
def dashboard(request: Request):
    context = {"ErrorNum": "WIP", "ErrorDetail": "Coming-Soon"}
    return render(request, "error.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Add User Functionality

@app.get("/adduser", response_class=HTMLResponse)
@login_required
def add_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "adduser.html")

#_________________________________________________________________________________________________________________________________________________________#

#Delete User Functionality

@app.get("/deleteuser", response_class=HTMLResponse)
@login_required
def delete_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "deleteuser.html")

@app.get("/getuser", response_class=HTMLResponse)
async def user_register(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    if hx_request is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    return render(request, "part-table.html", context)

@app.delete("/getuser/{username}", response_class=HTMLResponse)
async def user_delete(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username)
    if hx_request is None:
        return HTTPException(status_code=404)
    try:
        user.delete(synchronize_session=False) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    return render(request, "deleteuser.html")

#_________________________________________________________________________________________________________________________________________________________#

#Update User Functionality

@app.get("/updateuser", response_class=HTMLResponse)
@login_required
def update_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "updateuser.html")

@app.get("/getuserupdate", response_class=HTMLResponse)
async def user_register(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
        return redirect("/adminpanel")
    if hx_request is None:
        return HTTPException(status_code=404)
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    return render(request, "part-table-two.html", context)

@app.get("/contact/{id}/edit", response_class=HTMLResponse)
async def table_edit(request: Request, id: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if hx_request is None:
        raise HTTPException(status_code=404)
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    return render(request, "edit-table.html", context)

@app.put("/contact/{id}/update", response_class=HTMLResponse)
async def table_edit(request: Request, id: Optional[str], update: UpdateUser = Depends(UpdateUser.update_form), db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.id == id)
    user_data = user.first()
    update_data = {"id": user_data.id, "username": update.edited_username, "email": update.email, "isAdmin": update.isAdmin, "created_at": user_data.created_at}
    print(update_data)
    user.update(update_data, synchronize_session=False)
    db.commit()
    context = update_data
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "part-table-two.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Update all User Functionality
@app.get("/getalluser", response_class=HTMLResponse)
async def table_all(request: Request, db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    users_data = db.query(models.User).all()
    context = userdata_list(users_data)
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "getalluser-home.html", context)

@app.get("/getallusertable", response_class=HTMLResponse)
async def gettable_all(request: Request, db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    users_data = db.query(models.User).all()
    context = userdata_list(users_data)
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "getalluser-table.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Routers
app.include_router(auth.router)
