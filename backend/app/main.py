from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import company, product, conversation
from app.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

# create FastAPI app instance
app = FastAPI(
    title="Lekhak AI Backend",
    description="Backend API for Lekhak AI application",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we will restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Page Route
@app.get("/")
async def home():
    return {"data": "Welcome to the Lekhak AI Backend!"}


# Health Check Route
@app.get("/health")
async def health_check():
    return {"status": "OK"}


# Include Routers
app.include_router(company.router, prefix="/api/companies", tags=["companies"])
app.include_router(product.router, prefix="/api/products", tags=["products"])
app.include_router(
    conversation.router, prefix="/api/conversations", tags=["conversations"]
)
