from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.api.v1.endpoints import tasks
from app.db.session import engine
from app.api.v1.endpoints import auth 
# Lifecycle event to check DB connection on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check DB connection
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection established successfully.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    yield
    # Shutdown logic (if any) goes here

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="SDE-2 Assessment Submission",
    lifespan=lifespan
)

app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "task-manager"}