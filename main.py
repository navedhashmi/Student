from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import User
import models
from db_connection import engine, get_db, Se


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
async def homepage(request: Request, form_data: User = Depends(User.student_form), db: Se = Depends(get_db)):
    print(form_data.dict())
    context = {"request": request}
    return templates.TemplateResponse("home.html", context)
