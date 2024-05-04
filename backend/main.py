from fastapi import FastAPI, Request
from .calenderapiwrapper.main import CalendarAPIWrapper

app = FastAPI()

@app.get("/")
def rootRoute():
    return "You're successfully accessing to the FastAPI server."

@app.get("/register")
def register_entry(request: Request):
    pass

@app.get("/getToken")
def get_token(request: Request):
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")