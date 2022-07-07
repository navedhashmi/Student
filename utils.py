from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from config import get_settings


# Instance of Enviorment Variables
settings = get_settings()

#_____________________________________________________________________________________________________________________#

# Change the Output of App
def render(*args, **kwargs):
    response_text = settings.response_format
    if response_text == "json":
        return render_json(*args, **kwargs)
    elif response_text == "html":
        return render_html(*args, **kwargs)
    else:
        print("Invalid Response Format, Please Change the .env variable to either 'json' or 'html'")
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
def render_html(request, template_name, context={}, status_code:int=200, cookies:dict={}):
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

#_____________________________________________________________________________________________________________________#

#Jsonify Rendering Shortcut
def render_json(context={}, status_code:int=200, cookies:dict={}, response = JSONResponse):
    copy_context = context.copy()
    if type(copy_context) is list:
        copy_context = {"users": copy_context}
    else:
        copy_context.update({})
    send_response = response(copy_context, status_code=status_code)
    if len(cookies.keys()) > 0:
        for key, value in cookies.items():
            send_response.set_cookie(key=key, value=value, httponly=True)
    return send_response

#_____________________________________________________________________________________________________________________#

#Redirect Responses
def redirect(path, cookies:dict={}):
    response = RedirectResponse(path, status_code=302)
    for key, value in cookies.items():
            response.set_cookie(key=key, value=value, httponly=True)
    return response

#_____________________________________________________________________________________________________________________#

#SQL Query Row Object to List of Dics ( Used in endpoint to generate a list of dict to the command /getallusers )
def userdata_list(user_data):
    list_of_users = []
    for row in user_data:
        row_as_dict = row.__dict__
        row_as_dict.pop('_sa_instance_state', None)
        row_as_dict.pop('password', None)
        list_of_users.append(row_as_dict)
    return list_of_users


#_____________________________________________________________________________________________________________________#

#OpenAPI/SwaggerUI Tags
tags_metadata = [
    {
        "name": "JSONifiable",
        "description": "Endpoints that return JSONifiable data as per RESPONSE_FORMAT in .env",
    },
    {
        "name": "Non-JSONifiable",
        "description": "Endpoints that return only HTML",
    },
]

