from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional
from logging import getLogger, StreamHandler
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from gapi import gettoken, geturl
import os

from fastapi.responses import RedirectResponse

os.chdir(os.path.dirname(__file__))
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(  # for CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


@app.get("/", response_class=HTMLResponse)
async def root(req: Request):
    context = {"request": req}
    return templates.TemplateResponse("index.html", context)


@app.get("/auth")
async def auth():
    auth_url = geturl()
    return RedirectResponse(auth_url)


@app.get("/callback")
async def callback(code: Optional[str] = None):
    if code is None:
        raise HTTPException(
            status_code=400, detail="Code parameter is required")

    tok = gettoken(code)

    res = Response(content={"access_token": "tok"})
    # res.set_cookie(key="access_token", value=tok)

    return res
    # return {"access_token": tok}

if __name__ == "__main__":
    try:
        uvicorn.run("server:app", reload=True)
    except:
        pass
