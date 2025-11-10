from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="FEEDBACK SERVICE",
    description="User feedback and bug reports",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "37-feedback-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8129, reload=True)
