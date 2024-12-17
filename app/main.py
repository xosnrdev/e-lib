import datetime
import platform

from fastapi import FastAPI

app = FastAPI(
    title="E-Library API System",
    description="API for managing an online library system",
)


@app.get("/")
def health_check():
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
