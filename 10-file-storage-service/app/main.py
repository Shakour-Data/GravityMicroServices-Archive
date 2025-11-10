from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="FILE STORAGE SERVICE",
    description="File upload with CDN integration",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "10-file-storage-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8088, reload=True)
