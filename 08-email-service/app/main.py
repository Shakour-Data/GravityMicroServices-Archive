from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="EMAIL SERVICE",
    description="Dedicated email service with templates",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "08-email-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8086, reload=True)
