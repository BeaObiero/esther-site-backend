from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models
from app.db.database import engine
from app.routes import auth, contact, document, invoice, admin, booking

app = FastAPI(title="Esther Backend API")

# Create DB tables at startup
models.Base.metadata.create_all(bind=engine)

# CORS settings – limit to dev + prod domains
origins = [
    "http://localhost:3000",        # Local frontend
    "http://127.0.0.1:3000",
    "https://estherwaweru.com"      # Live frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(document.router, prefix="/api/documents", tags=["Documents"])
app.include_router(invoice.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(booking.router, prefix="/api", tags=["Booking"])


# Health check
@app.get("/")
def read_root():
    return {"message": "Welcome to Esther's Backend API!"}
