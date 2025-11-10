from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="REVIEW SERVICE",
    description="Product reviews and ratings",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "21-review-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8106, reload=True)
