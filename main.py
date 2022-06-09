from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from schemas import User

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("home.html", context)

@app.post("/", response_class=HTMLResponse)
async def homepage(request: Request, form_data: User = Depends(User.student_form)):
    print(form_data)
    context = {"request": request}
    return templates.TemplateResponse("home.html", context)