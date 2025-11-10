from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="TRANSLATION SERVICE",
    description="Multi-language support",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "35-translation-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8127, reload=True)
