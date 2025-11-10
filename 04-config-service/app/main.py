from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="CONFIG SERVICE",
    description="Centralized configuration management",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "04-config-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8090, reload=True)
