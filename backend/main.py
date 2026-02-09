import os
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from app.routers import router

load_dotenv()

app = FastAPI(
    title="Instant Dashboard App"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://instant-dashboard-app.vercel.app/", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "status": status.HTTP_200_OK,
        "model": "groq/llama-3.3-70b-versatile",
        "endpoints": {
            "generate": "/generate-dashboard",
            "health": "/health"
        },
        "detail": "Running successfully..."
    }

@app.get("/health")
async def health():
    """
        endpoint for check the health of the app
    """
    try:
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unhealthy: GROQ_API_KEY not set")
        return {"status": status.HTTP_200_OK, "detail": "Healthy: You may start"}
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)