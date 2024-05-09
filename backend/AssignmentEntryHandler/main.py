from fastapi import FastAPI

class assignmentEntryReceiver:
    def __init__(self, app:FastAPI = FastAPI()):
        self.APP = app

    def defEndpoint():
        pass

class assignmentEntryHandler:
    def __init__(self, receiver):
        self.receiver = receiver

    def handle(self, assignment):
        pass