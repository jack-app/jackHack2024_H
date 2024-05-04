from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def rootRoute():
    return "You're successfully accessing to the FastAPI server."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port="61000")