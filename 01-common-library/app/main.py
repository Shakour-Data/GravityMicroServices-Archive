from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="COMMON LIBRARY",
    description="Shared utilities and base models",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "01-common-library"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=N/A, reload=True)
