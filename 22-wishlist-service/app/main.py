from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="WISHLIST SERVICE",
    description="User wishlists and collections",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "22-wishlist-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8107, reload=True)
