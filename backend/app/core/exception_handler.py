from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
import logging
logger=logging.getLogger(__name__)
async def http_exception_handler(

    request: Request,

    exc: StarletteHTTPException

):

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "message": exc.detail

        }

    )




async def validation_exception_handler(

    request: Request,

    exc: RequestValidationError

):

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "message": "Validation Error",

            "errors": exc.errors()

        }

    )

async def sqlalchemy_exception_handler(

    request: Request,

    exc: SQLAlchemyError

):

    logger.exception(exc)

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": "Database Error"

        }

    )

async def generic_exception_handler(

    request: Request,

    exc: Exception

):

    logger.exception(exc)

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": "Internal Server Error"

        }

    )