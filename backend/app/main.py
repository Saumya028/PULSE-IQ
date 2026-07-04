from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from routes.industry import router as industry_router
from routes.intelligence import router as intelligence_router
from routes.dashboard import router as dashboard_router
from routes.executive_brief import router as executive_brief_router

import models.article
import models.executive_brief
import models.industry
import models.intelligence
import models.source

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PulseIQ API",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://pulse-iq-4p4e.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PulseIQ Backend Running 🚀"}

app.include_router(industry_router)
app.include_router(intelligence_router)
app.include_router(dashboard_router)
app.include_router(executive_brief_router)