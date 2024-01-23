from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.admin import api as admin

app = FastAPI(
    title="Project",
    description="APIs for Project",
    version="1.0.0",
    # redoc_url=None,
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        error = exc.errors()[-1]
        field = str(error["loc"][-1])
        message = error["msg"]
        detail = field + " - " + message.capitalize()
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": detail}),
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
