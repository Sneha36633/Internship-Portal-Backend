from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import engine, Base
from .models import User, Skill, Company, Internship, Recommendation
from .routers import (
    auth_router,
    users_router,
    skills_router,
    companies_router,
    internships_router,
    recommendations_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Internship Portal API",
    description="API for an AI-powered internship recommendation platform.",
    version="1.0.0",
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://internship-portal-sandy.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router.router, prefix="/api", tags=["Users"])
app.include_router(skills_router.router, prefix="/api", tags=["Skills"])
app.include_router(companies_router.router, prefix="/api", tags=["Companies"])
app.include_router(internships_router.router, prefix="/api", tags=["Internships"])
app.include_router(recommendations_router.router, prefix="/api", tags=["Recommendations"])

@app.get("/")
def read_root():
    return {"status": "API is running successfully"}