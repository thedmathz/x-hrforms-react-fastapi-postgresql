import datetime
from fastapi import HTTPException

def response_api(status: int, message: str = None, name: str = None):
    names = {
        0: name,
        200: "Ok",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        500: "Internal Server Error"
    }
    messages = {
        0: message,
        200: "",
        400: "Invalid request parameters.",
        401: "Authentication credentials were missing or invalid.",
        403: "You do not have permission to access this resource.",
        404: "The requested resource could not be found.",
        409: "Record already exists.",
        500: "An unexpected error occurred."
    }

    response_body = { "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() }

    if status >= 400:
        response_body['name'] = name if name is not None else names.get(status, "UNKNOWN")
        response_body['message'] = message if message else messages.get(status, "Unknown error.")
        raise HTTPException(status_code=status, detail=response_body)
    return response_body
