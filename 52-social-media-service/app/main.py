from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="SOCIAL MEDIA SERVICE",
    description="Social login and sharing",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "52-social-media-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8154, reload=True)
