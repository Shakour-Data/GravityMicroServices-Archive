from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="SEARCH SERVICE",
    description="Full-text search with filters",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "19-search-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8104, reload=True)
