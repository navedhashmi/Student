from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

#_____________________________________________________________________________________________________________________#

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Password Hashing
def hash(password: str):
    return pass_context.hash(password)

#Password Verification
def verify(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)

#_____________________________________________________________________________________________________________________#

templates = Jinja2Templates(directory="templates")

#Template Rendering Shortcut
def render(request, template_name, context={}, status_code:int=200, cookies:dict={}):
    copy_context = context.copy()
    if type(copy_context) is list:
        copy_context = {"request": request, "users": copy_context}
    else:
        copy_context.update({"request": request})
    template_to_render = templates.get_template(template_name)
    html_context = template_to_render.render(copy_context)
    response = HTMLResponse(html_context, status_code=status_code)
    if len(cookies.keys()) > 0:
        for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)
    return response


#Redirect Responses
def redirect(path, cookies:dict={}):
    response = RedirectResponse(path, status_code=302)
    for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)
    return response

#_____________________________________________________________________________________________________________________#

#SQL Query Row Object to List of Dics

def userdata_list(user_data):
    list_of_users = []
    for row in user_data:
        row_as_dict = row.__dict__
        row_as_dict.pop('_sa_instance_state', None)
        row_as_dict.pop('password', None)
        list_of_users.append(row_as_dict)
    return list_of_users


