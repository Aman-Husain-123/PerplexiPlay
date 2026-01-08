import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from backend.routes import auth
from backend.core.firebase import initialize_firebase

# Initialize Firebase Admin SDK
initialize_firebase()

app = FastAPI(title="PerplexiPlay API (MongoDB)", version="0.1.0")

# Include routes
app.include_router(auth.router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
