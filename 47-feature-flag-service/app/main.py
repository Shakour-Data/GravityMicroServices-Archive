from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="FEATURE FLAG SERVICE",
    description="Feature toggles and gradual rollout",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "47-feature-flag-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8149, reload=True)
