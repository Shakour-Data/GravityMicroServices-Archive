from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="REFERRAL SERVICE",
    description="Referral program tracking",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "34-referral-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8126, reload=True)
