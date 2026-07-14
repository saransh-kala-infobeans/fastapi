#endpoint is the unique combination of URL + an HTTP method, which identifies/trigger a specific function.
#path is the URL part after domain. ex: '/' or '/tasks' etc.
#A route is the mapping of an endpoint with a handler function.


from fastapi import FastAPI, Header, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated

#Pydantic is a popular Python library used for data validation and parsing. It ensures that the data flowing into and out of your application matches the expected types and formats, making your code significantly more robust. BaseModel is the core class in Pydantic that you inherit from to define the structure of your data.

#Better to use Pydantic rather than Dataclasses because dataclasses doesn't provide build-in validation and also doesn't enforce typehints at runtime..

class Task(BaseModel):
    taskID : int
    title : str
    completed : bool = False

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username : str
    password : str

app = FastAPI(
    title= "Saransh's API project",
    summary= "This is the summary",
    description="""
## HEHE double hash.
**inside the double asterisk right now**

##YO
""",
version="1.2.3.4",
terms_of_service="https://google.com",
contact={
    "name" : "Saransh kala",
    "email" : "saransh@contact.com"
},
license_info={
    "name": "FastAPI documentation link",
    "url":"https://fastapi.tiangolo.com/",
}
)



tasks : list[Task] = []

#for authorization., putting this above here, because of python's syntax thing, if I am function from some another function,
#then the called function should be present in the code BEFORE/ABOVE the calling function.
def get_current_user(authorization: str = Header(default= None)):
    if authorization is None:
        raise HTTPException(status_code= 401, detail= "Not authenticated")

    
    #found during testing. that authorization.split(" ")[1] could throw error resulting in internal server error.
    #occurs when user only write "Bearer" (no token).

    #this code helps us surpass that problem.
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format. Use: Bearer <token>")

    try:
        #earlier
        #token = authorization.split(" ")[1]

        token = parts[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username = payload.get("username")

        if username is None:
            raise HTTPException(status_code= 401, detail= "Invalid token")
        
        return username
    except JWTError:
        raise HTTPException(status_code= 401, detail= "Invalid or expired token")


@app.get("/")   #this whole thing = decorater
def home():  #handler function
    return {
        "route" : "/",
        "route handler" : "this is the route handler function named home()"
    }


'''
This is just a redundant function to learn about headers, that's it.
Headers : Headers are key-value pairs sent along with a request or response that
          provide metadata (information about the data).
example:
Content-Type: application/json
Authorization: Bearer abc123
'''
@app.get("/about")
def about(header_object = Header()):
    #remember, Header() is not a constructor, it's a function, or to say a factory function provided by fastAPI, which returns a special python that tells fastapi to extract the perimeter form request headers.
    #Python exectues Header() once, when the function is defined, not when the request arrives.
    return {
        "header-object_information" : header_object,
        "result" : "welcome, this is the about route"
    } 
'''
Explanation about the header object.
basically, we use this technique, when we want a specific named header from all the headers received in the request..
Header() : FastAPI dependency for reading headers.
means, when we write  
    header_object = Header() in the parameter.
we are asking fastAPI, that, go to the headers, which were received along with the request, and find me 
the one which is named as 'header-object', once found, put the value associated with this head-object inside
the header_object variable present in the parameter.

say we sent a request which has headers like:
application-type: application/json
header-object: hello
then, on execution, header_object = "hello"

also, this process is case-insensitive, meaning, | HEADER_object: hello  |<== this will also work.


(notice, underscore became hyphen, fastAPI converts this automatically. 
because convential way to give names to headers is something-something.. we just use underscore in code because 
python doesn't allow the put hyphen in variable names, fastAPI helps us by later converting/using it as hyphen.)

one more thing about header, they are always received as text, it is fastAPI which coverts them
HTTP headers are always sent as text (strings).

say:
def about(active: bool = Header()):
    ...

we get request with header:
Active: true
then, fastAPI converts it, "true"-> True (boolean)


Another efficient way to play with headers is.
code:

from fastapi import Request
@app.get("/about")
def about(request: Request):
    return {"headers": dict(request.headers)}

here, Once fastAPI see type hint as 'Request' here, it'll automatically put the Request object here.
These is NOT a query/path parameter.
then you can use, 
request.headers, it behaves like a dictionary.
    request.headers["header-object"]
    request.headers.get("header-object")

request.url    etc things.
'''


@app.get("/random") 
def random(request: Request):
    headers = dict(request.headers)
    return {
        "headers" : headers
    }


# "/tasks" Endpoints below 
@app.get("/tasks")
def get_all_tasks():
    return {
        "tasks" : tasks
    }

@app.post("/tasks")
def add_task(task : Task, current_user = Depends(get_current_user)):
    for t in tasks:
        if t.taskID == task.taskID:
            raise HTTPException(
                status_code=409, 
                detail=f"409Conflict, Duplicate, task with ID {task.taskID} already exists.")
    
    tasks.append(task)
    return {
        "result" : "task added successfully."
    }

@app.put("/tasks/{task_id}")
def modify_existing_task(task_id : int, task : Task):
    #check if tasks list is empty
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found. List's empty.")

    #modify task
    for t in tasks:
        if task_id == t.taskID:
            t.title = task.title
            t.completed = task.completed
            return {
                "result" : "done"
            }
    #raise exception if no task with corresponding taskID found in the list.
    raise HTTPException(
        status_code = 404,
        detail= f"task with task id {task_id} not found."
    )

@app.get("/raise-exception-404")
def raise_exp():
    raise HTTPException(
        status_code= 404,
        detail = "hello, we ourselves are raising this exception, there's no necessary error, or anything."
    )

@app.get("/tasks/{task_id}")
def get_specific_task(task_id : int):
    if tasks:
        for task in tasks:
            if task.taskID == task_id:
                return {
                    "Desired task" : task
                } 
        raise HTTPException(
            status_code= 404, 
            detail = "task not found"
        )
    else:
        raise HTTPException(status_code=404, detail="No tasks found.")

#
@app.delete("/tasks/{id}")
def delete_task(id : int):
    task_to_delete = None
    if tasks:
        for t in tasks:
            if t.taskID == id:
                task_to_delete = t 
        
        if task_to_delete is not None:
            tasks.remove(task_to_delete)
            return {
                "result" : f"task with task id {id} deleted successfully."
            }
        else :
            raise HTTPException(
                status_code = 404,
                detail = "Invalid task id, no task with such id present in the database"
            )
    else:
        raise HTTPException(status_code=404, detail="No tasks found. List's empty.")


@app.patch('/tasks/{task_id}/status')
def update_task_status(task_id : int):
    if tasks:
        for task in tasks:
            if task.taskID == task_id:
                task.completed = not task.completed
                return {
                    "result" : "changed status successfully"
                } 
        raise HTTPException(
            status_code= 404, 
            detail = "task not found"
        )
    else:
        raise HTTPException(status_code=404, detail="No tasks found. List's empty.")


#starting with authenticaiton in fastAPI
#using Depends and depends injection.
#form fastapi import Depends
#from passlib.context import CryptContext
#from jose import jwt, JWTError
#from datetime import datetime, timedelta

#Configuration.
#HS256 is the algorithm used to create the signature. 
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

#password hashing setup
#CryptContext is a hashing utility from the passlib library. We're creating an instanse of it and storing it in pwd_context.
#schemes["bcrypt"] <- tells which hashing algorithm to use. brypt is one of the most trusted and widely used algorithm for hashing passwords.
pwd_context = CryptContext(schemes=["bcrypt"])

# what is .hash()
#hashing is a one way transformation of a string into a fixed scrambled output. meaning,
# pwd_context.hash("1234")  →  "$2b$12$eKpBMqvQdnO1qmRtW9vXuOWRkl..."
#ONE-WAY means, you can never reverse it back to 1234. EVER. So when a user logs in with password "1234", instead of doing "1234"=="1234"
#we do, pwd_context.verify("1234", hased_password)
#what verify does is, it hashes the incoming password, and compares it with the stored hash-- without ever storing or comparing plain text.

#WHY do we not store plain text?
#Because, if your database ever gets hacked.
#then if the pass is stored as a plain text, the hacker can directly see it, game over.
#hence we store hashed password.

#REMEMBER ONE THING
#
#**   HASHING IS NOT ENCODING     **#
#
#because encoding can be reversed/decoded. It is designed to be reversible.
#For example: Base64 from JWT. it is reversible.

#HASHING is different, it's a mathematically ONE-WAY function--meaning, there's no reverse operation. Even the creators of bcrypt can't reverse it.

#bcrypt salt method for identical passwords.
# Registration:
# "1234" + random_salt  →  bcrypt  →  "$2b$12$<salt><hash>"  →  stored in DB

# Login:
# "1234" incoming
#         ↓
# extract salt from "$2b$12$<salt><hash>"
#         ↓
# "1234" + extracted_salt  →  bcrypt  →  compare with stored  →  match 


##ACTUAL IMPLEMENTATION NOW
##LOGIN ENDPOINT.
##A LoginRequest class has been made (on the top of the code in this module itself)

#setting up a in-memory database for users.
fake_users = {
    "john": {
        "username": "john",
        "hashed_password": pwd_context.hash("1234")  # hashing the password
    }
}

@app.post("/register")
def register(req : RegisterRequest):
    if not req.password:
        raise HTTPException(
            status_code= 400, 
            detail= "The password field cannot be empty."
        )
    
    #status code 400 : BAD REQUEST ERROR, the server cannot process the request due to client side errors.
    if len(req.password) < 8:
        raise HTTPException(
            status_code= 400,
            detail= "The password length must be >= 8."
        )

    if req.username in fake_users:
        raise HTTPException(
            status_code= 409,
            detail= "User with this username already exists in user database."
        )

    fake_users[req.username]= {
        "username" : req.username,
        "hashed_password" : pwd_context.hash(req.password)
    }

    return {
        "result" : f"{req.username} registered successfully." 
    }

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire   #to_encode = {"username": ___ , "exp": ___ }
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
#to_encode ===> payload
#python-jose library handles the header.
#header is created automatically in bg, which looks something like= {"alg": "HS256", "typ": "JWT"}
#

@app.post("/login")
def login(request: LoginRequest):
    #check if user exits. 
    user = fake_users.get(request.username)

    #check if user exists in database, using their username.
    if not user:
        raise HTTPException(status_code= 401, detail= "Invalid credentials")
    
    #check if password is correct
    if pwd_context.verify(request.password, user["hashed_password"]) == False:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    token = create_token({"username": request.username})
    return {
        "access_token" : token
    }

#just to be able to commit on git
@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return{
        "message": f"Hello {current_user}, you are authenticated."
    }

# OAuth2 Starts from here.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'token')
# @app.get("/temp-items")
# def temp_read_items(token : Annotated[str, Depends(oauth2_scheme)]):
#     return {
#         "token" : token
#     }