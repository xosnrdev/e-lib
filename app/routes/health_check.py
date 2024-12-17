import datetime
import platform

from fastapi import APIRouter, Request

router = APIRouter(tags=["Health Check"])


@router.get("/")
def health_check(request: Request):
    """
    Provides a health check endpoint to verify the system's operational status.

    **Endpoint:** GET /

    **Responses:**
        - 200 OK: Returns system information and operational status.
    """
    app = request.app
    return {
        "name": app.title,
        "version": app.version,
        "description": app.description,
        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "operational",
    }
