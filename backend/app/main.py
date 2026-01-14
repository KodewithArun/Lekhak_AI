import warnings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import company, content, conversation, framework, product
from app.utils.loggers import get_logger

warnings.filterwarnings("ignore", category=Warning)

logger = get_logger("main")

# create FastAPI app instance
app = FastAPI(
    title="Lekhak AI Backend",
    description="Backend API for Lekhak AI application",
    version="1.0.0",
)

logger.info("FastAPI application instance created")


# Create all tables on startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created (if not exist)")


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
app.include_router(framework.router, prefix="/api/frameworks", tags=["frameworks"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
