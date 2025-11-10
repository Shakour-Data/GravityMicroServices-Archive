from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="WEBHOOK SERVICE",
    description="Webhook management and delivery",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "41-webhook-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8143, reload=True)
