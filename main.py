from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import NewUser
import models, auth
from utils import hash
from db_connection import engine, get_db, Se #Se = Session imported from db_connection


# Models Execution
models.Base.metadata.create_all(bind=engine)


#FastAPI app instance
app = FastAPI()

#Jinja2Templates instance = Getting Static and HTML Files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#API Calls
@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("home.html", context)

@app.post("/", response_class=HTMLResponse)
async def homepage(request: Request, form_data: NewUser = Depends(NewUser.register_form), db: Se = Depends(get_db)):
    form_data.password = hash(form_data.password)
    new_user = models.User(**form_data.dict())
    print(new_user.password)
    try:
        db.add(new_user) 
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or Username is already in Database")
    context = {"request": request}
    return templates.TemplateResponse("home.html", context)

#Routers
app.include_router(auth.router)
