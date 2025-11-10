from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="AB TESTING SERVICE",
    description="A/B test management",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "46-ab-testing-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8148, reload=True)
