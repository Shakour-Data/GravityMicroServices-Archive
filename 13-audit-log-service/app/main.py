from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="AUDIT LOG SERVICE",
    description="Comprehensive audit logging",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "13-audit-log-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8089, reload=True)
