from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="INVENTORY SERVICE",
    description="Stock management and tracking",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "25-inventory-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8110, reload=True)
