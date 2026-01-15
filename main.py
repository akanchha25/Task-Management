from fastapi import FastAPI
from app.api.v1.endpoints import tasks

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="SDE-2 Assessment Submission"
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "task-manager"}