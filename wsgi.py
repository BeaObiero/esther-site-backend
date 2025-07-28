
from app.main import app

# Expose `app` so Flask CLI can detect it
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
