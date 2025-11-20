from fastapi import FastAPI
from app.routes.webhook import router as webhook_router

# Create the FastAPI app instance
app = FastAPI()

# Simple health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include the webhook routes (even if empty for now)
app.include_router(webhook_router)
