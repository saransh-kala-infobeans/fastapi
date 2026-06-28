#endpoint is the unique combination of URL + an HTTP method, which identifies/trigger a specific function.
#path is the URL part after domain. ex: '/' or '/tasks' etc.
#A route is the mapping of an endpoint with a handler function.


from fastapi import FastAPI 
from pydantic import BaseModel
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request

class Task(BaseModel):
    taskID : int
    title : str
    completed : bool = False

app = FastAPI()
tasks : list[Task] = []


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
    return {
        "header-object_information" : header_object,
        "result" : "welcome, this is the about route"
    } 
'''
Explanation about the header object.
basically, we use this technique, when we want a specific named header from all the headers.
Header() : FastAPI dependency for reading headers.
means, when we write  
    header_object = Header() in the parameter.
we are asking fastAPI, that, go to the headers, which came along with the request, and find me 
the one which is named as 'head-object', once found, put the value associated with this head-object inside
the header_object variable present in the parameter.

say we sent a request which has headers like:
application-type: application/json
header-object: hello
then, on execution, header_object = "hello"

also, this process is case-insensitive, meaning, | HEADER_object: hello  |<== this will also work.


(notice, underscore became hyphen, fastAPI converts this automatically. 
because convential way to give names to headers is something-something we just use underscore in code because 
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
    request.headers["header-objects"]
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
def add_task(task : Task):
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