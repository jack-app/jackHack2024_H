from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

class Server:
    def __init__(self, app:FastAPI=FastAPI()):
        self.APP = app
        self.APP.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "https://accounts.google.com/*",
                "https://tact.ac.thers.ac.jp/*"
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self.defEndpoints()

    def defEndpoints(self):
        @self.APP.get("/")
        def root():
            return {"msg":"You're successfully accessing to the FastAPI server."}

    def run(self):
        import uvicorn
        uvicorn.run(self.app, port="61000")