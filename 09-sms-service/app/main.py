from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="SMS SERVICE",
    description="SMS delivery via Twilio/AWS SNS",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "09-sms-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8087, reload=True)
