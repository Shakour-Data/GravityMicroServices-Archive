from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="EXPORT SERVICE",
    description="Data export in multiple formats",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "42-export-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8144, reload=True)
