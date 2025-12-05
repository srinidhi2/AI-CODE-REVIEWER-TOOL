from fastapi import FastAPI
from app.routes.webhook import router as webhook_router
from app.services.ai_service import review_code
# Create the FastAPI app instance
app = FastAPI()

# Simple health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# temporary endpoint to test the AI service
@app.get("/test-ai")
def test_ai():
    # Fake code diff (simulating a small PR change)
    fake_diff = """
    diff --git a/calculator.py b/calculator.py
    index e69de29..b6fc4c9 100644
    --- a/calculator.py
    +++ b/calculator.py
    @@ -0,0 +1,12 @@
    +def add(a, b):
    +    return a + b
    +
    +def divide(a, b):
    +    # TODO: handle division by zero
    +    return a / b
    """

    feedback = review_code(fake_diff)
    return {"feedback": feedback}




# Include the webhook routes (even if empty for now)
app.include_router(webhook_router)
