from typing import Callable,Any
from fastapi import Response

def handlerErrorAsHTTPResponse(trial:Callable[[],Any], response:Response):
    try:
        return trial()
    except Exception as e:
        if hasattr(e, "http_status"):
            response.status_code = e.http_status
        return {"msg":str(e)}        
    