from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.api import auth, audit

app = FastAPI(title="CodeSentinel AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Register Routers
app.include_router(auth.router)
app.include_router(audit.router)  # 👈 Added Audit Router

@app.get("/")
def root():
    return {
        "service": "CodeSentinel AI",
        "status": "online",
        "docs_url": "/docs"
    }