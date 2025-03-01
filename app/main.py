import uvicorn
from fastapi import FastAPI
from api import  task, user

app = FastAPI(title="Smart Task Scheduler")

app.include_router(task.router, prefix='/tasks', tags=['tasks'])
app.include_router(user.router, prefix='/users', tags=['users'])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    # Run without reload for debugging
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=False)