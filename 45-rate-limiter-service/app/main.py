from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="RATE LIMITER SERVICE",
    description="Distributed rate limiting",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "45-rate-limiter-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8147, reload=True)
