from typing import Optional
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi import FastAPI, Header, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from decorators import login_required
from utils import redirect, render
from schemas import NewUser, UpdateUser
import models, auth, middleware, requests
from utils import hash, userdata_list, tags_metadata
from config import get_settings
from starlette.exceptions import HTTPException as HTTPStarException
from db_connection import engine, get_db, Se #Se = Session imported from db_connection

# Models Execution
models.Base.metadata.create_all(bind=engine)

#FastAPI app instance
app = FastAPI(openapi_tags=tags_metadata)
app.add_middleware(AuthenticationMiddleware, backend=middleware.JWTCookieBackend())
app.mount("/static", StaticFiles(directory="static"), name="static")


#Exception-Handler
@app.exception_handler(HTTPStarException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = "error.html"
    context = {"ErrorNum": status_code, "ErrorDetail": "Error"}
    return render(request, template_name, context, status_code=status_code)

# Instance of Enviorment Variables
settings = get_settings()

# Change the response_class of App between json and html
def response_format():
    response_text = settings.response_format
    if response_text == "json":
        return JSONResponse
    elif response_text == "html":
        return HTMLResponse
    else:
        print("Invalid Response Format, Please Change the .env variable to either 'json' or 'html'")


#API Calls

#_________________________________________________________________________________________________________________________________________________________#

#####################___Homepage__#####################

@app.get("/", tags=["JSONifiable"], response_class=response_format())
def homepage(request: Request):
    context = {"Homepage": "User Login and Registration"}
    if response_format() == JSONResponse:
        return render(context)
    else:
        return render(request, "home.html", context)

#####################___Register | Add__#####################

@app.post("/register", tags=["JSONifiable"], response_class=response_format()) # This Call used in Add User
async def user_register(request: Request, form_data: NewUser = Depends(NewUser.register_form), db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    form_data.password = hash(form_data.password)
    new_user = models.User(**form_data.dict())
    try:
        db.add(new_user) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Username is already Registered")
    if hx_request: # If hx_request, then it means that the user is coming from the HX-adminpanel page
        context = {"Successful": f"{new_user.username} Added into the Database by Admin"}
        return render(request, "adduser.html", context)
    context = {"Successful": f"{new_user.username} Registered Successfully"}
    if response_format() == JSONResponse:
        return render(context)
    else:
        url = "https://http-api-2022.azurewebsites.net:443/api/fast-api-workflow/triggers/manual/invoke?api-version=2022-05-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=yID1wk7brBdxmpltXrI2erDuD3wnohdXJLvP9vObuNA"
        headers = {'Content-Type': 'application/json'}
        requests.post(url, json={"name": new_user.username, "email": new_user.email}, headers=headers)
        return render(request, "home.html", context)

#API Calls : Require User Login
#_________________________________________________________________________________________________________________________________________________________#

#####################___AdminDashboard-Home__#####################

@app.get("/adminpanel", tags=["JSONifiable"], response_class=response_format())
#@requires(['admin'])
@login_required
def admin_home(request: Request):
    context = {"Homepage": "Admin Dashboard"}
    if response_format() == JSONResponse:
        return render(context)
    else:
        return render(request, "admin.html", context)
       
#####################___AdminDashboard-NavBar-Buttons__#####################
# Dashboard WIP
@app.get("/admindashboard", tags=["Non-JSONifiable"], response_class=HTMLResponse)
@login_required
def dashboard(request: Request):
    context = {"ErrorNum": "WIP", "ErrorDetail": "Coming-Soon"}
    return render(request, "error.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Add User Functionality

@app.get("/adduser", tags=["Non-JSONifiable"], response_class=HTMLResponse)
@login_required
def add_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "adduser.html")

#_________________________________________________________________________________________________________________________________________________________#

#Delete User Functionality

@app.get("/deleteuser", tags=["Non-JSONifiable"], response_class=HTMLResponse)
@login_required
def delete_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "deleteuser.html")

@app.get("/getuser", tags=["JSONifiable"], response_class=response_format())
async def user_register(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    if hx_request is None and response_format() == HTMLResponse:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    if response_format() == JSONResponse:
        context["created_at"] = str(context["created_at"])
        return render(context)
    else:
        return render(request, "part-table.html", context)   

@app.delete("/getuser/{username}", tags=["JSONifiable"], response_class=response_format())
async def user_delete(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username)
    if hx_request is None and response_format() == HTMLResponse:
        return HTTPException(status_code=404)
    try:
        user.delete(synchronize_session=False) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {username} not in System")
    context = {"Successful": f"{username} Deleted Successfully"}
    if response_format() == JSONResponse:
        return render(context)
    else: 
        return render(request, "deleteuser.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Update User Functionality

@app.get("/updateuser", tags=["Non-JSONifiable"], response_class=HTMLResponse)
@login_required
def update_user(request: Request, hx_request: Optional[str] = Header(None)):
    if hx_request is None:
        raise HTTPException(status_code=404)
    return render(request, "updateuser.html")

@app.get("/getuserupdate", tags=["Non-JSONifiable"], response_class=HTMLResponse)
async def user_register(request: Request, username: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return redirect("/adminpanel")
    if hx_request is None:
        return HTTPException(status_code=404)
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    return render(request, "part-table-two.html", context)

@app.get("/contact/{id}/edit", tags=["Non-JSONifiable"], response_class=HTMLResponse)
async def table_edit(request: Request, id: Optional[str], db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if hx_request is None:
        raise HTTPException(status_code=404)
    context = {"id": user.id, "username": user.username, "email": user.email, "isAdmin": user.isAdmin, "created_at": user.created_at}
    return render(request, "edit-table.html", context)

@app.put("/contact/{id}/update", tags=["JSONifiable"], response_class=response_format())
async def table_edit(request: Request, id: Optional[str], update: UpdateUser = Depends(UpdateUser.update_form), db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    user = db.query(models.User).filter(models.User.id == id)
    user_data = user.first()
    update_data = {"id": user_data.id, "username": update.edited_username, "email": update.email, "isAdmin": update.isAdmin, "created_at": user_data.created_at}
    user.update(update_data, synchronize_session=False)
    db.commit()
    context = update_data
    if hx_request is None and response_format() == HTMLResponse:
        raise HTTPException(status_code=404)
    if response_format() == JSONResponse:
        context["created_at"] = str(context["created_at"]) # Convert datetime to string to tackle (TypeError: Object of type datetime is not JSON serializable)
        return render(context)
    else: 
        return render(request, "part-table-two.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Get all User Functionality
@app.get("/getalluser", tags=["JSONifiable"], response_class=response_format())
async def table_all(request: Request, db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    users_data = db.query(models.User).all()
    context = userdata_list(users_data)
    if hx_request is None and response_format() == HTMLResponse:
        raise HTTPException(status_code=404)
    if response_format() == JSONResponse:
        for x in context:
            x["created_at"] = str(x["created_at"])
        return render(context)
    else: 
        return render(request, "getalluser-home.html", context)

@app.get("/getallusertable", tags=["Non-JSONifiable"], response_class=HTMLResponse)
async def gettable_all(request: Request, db: Se = Depends(get_db), hx_request: Optional[str] = Header(None)):
    users_data = db.query(models.User).all()
    context = userdata_list(users_data)
    if hx_request is None and response_format() == HTMLResponse:
        raise HTTPException(status_code=404)
    return render(request, "getalluser-table.html", context)

#_________________________________________________________________________________________________________________________________________________________#

#Routers
app.include_router(auth.router)