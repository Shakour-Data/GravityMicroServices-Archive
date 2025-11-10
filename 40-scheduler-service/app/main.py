from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="SCHEDULER SERVICE",
    description="Job scheduling and background tasks",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "40-scheduler-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8142, reload=True)
