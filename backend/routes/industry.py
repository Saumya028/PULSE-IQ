from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from services.pipeline_service import PipelineService

router = APIRouter(
    prefix="/industry",
    tags=["Industry"]
)


class IndustryRequest(BaseModel):
    industry: str


@router.post("/search")
def search_industry(
    request: IndustryRequest,
    db: Session = Depends(get_db)
):
    pipeline = PipelineService()

    results = pipeline.run_pipeline(
        db=db,
        industry=request.industry
    )

    return {
        "industry": request.industry,
        "count": len(results),
        "results": results
    }