from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="CMS SERVICE",
    description="Content management system",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "36-cms-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8128, reload=True)
