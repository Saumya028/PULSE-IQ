from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from models.executive_brief import ExecutiveBrief

router = APIRouter(
    prefix="/brief",
    tags=["Executive Brief"]
)


@router.get("/{industry}")
def latest_brief(
    industry: str,
    db: Session = Depends(get_db)
):

    brief = (
        db.query(ExecutiveBrief)
        .filter(
            ExecutiveBrief.industry.ilike(industry)
        )
        .order_by(
            ExecutiveBrief.generated_at.desc()
        )
        .first()
    )

    if brief is None:
        raise HTTPException(
            status_code=404,
            detail=f"No executive brief found for '{industry}'. Run the pipeline first."
        )

    return {
        "industry": brief.industry,
        "headline": brief.headline,
        "summary": brief.summary,
        "key_trends": brief.key_trends,
        "recommended_actions": brief.recommended_actions,
        "generated_at": brief.generated_at
    }