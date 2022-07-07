# Student Record
(A FastAPI based Student Hub (Work In Progress))

## Project Description
The Project aim is to develop a Student Hub where each student can register an account with access to various study related feature and tools. The Feature and Tools are still in development.

## Tech-Used

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Unicorn
- HTMX
- Jinja2Templates
- etc..

## Downloads

> "Requirements.txt", [Download](https://mega.nz/file/p8sXWSyI#mCMACLkSWz8fibXNMYAGPbhELvDZKiLfMWkdjEQ9BU4)

## Steps to Run the project

+ ### Prerequisite
  + Make sure you downloaded the Requirements.txt from project file or from above link.
  + After Downloading, install the required libraries and modules with the help of pip install Requirements.txt
  + Note: It is recommended to use a Venv(Virtual Environment) and then follow above two steps.
  
+ ### Setting up Environment Variables (Update as on 07/07/2022)
  + Make a new .env file into your project folder.
  + Configure it as per below picture.
  + A new "RESPONSE_FORMAT" is added in the .env file to determine the output of the App, Change it into "json" to get JsonResponse in (Swagger | OpenAPI) docs or set it to "html" for normal website responses. (More info on SwaggerUI Tags)
  
  
  ![](https://i.ibb.co/cYfDdqn/env.png)
  
+ ### Command to start uvicorn server
  + `uvicorn main:app --reload`

# Update(07-07-2022)
## JSONifiable and Non-JSONifiable
JSONifiable and Non-JSONifiable is the Output of the App, set as per the "RESPONSE_FORMAT" in .env(Environment Variable File)
+ ### JSONifiable:
   + Set `"RESPONSE_FORMAT=json"` to get JSON response in OPENapi/Swagger UI on JSONifiable endpoint.
   + Set `"RESPONSE_FORMAT=html"` to get normal HTML output on each JSONifiable endpoint.
+ ### Non-JSONifiable
   + They'll return just HTML output as there isn't anything useful to return as JSON.


## OpenAPI - Tags
  ![](https://i.ibb.co/K60WXN5/jasonifiable.png)
  + Tags with JSONifiable will return JSON Response as per "RESPONSE_FORMAT"
  
# Project Structure | Folder Structure | Description of Files (WIP - Coming Soon) 
