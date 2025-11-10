from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="CHAT SERVICE",
    description="Real-time messaging with WebSocket",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "28-chat-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8120, reload=True)
