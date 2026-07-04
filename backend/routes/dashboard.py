from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from models.intelligence import Intelligence

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ---------------------------------------------------------
# Latest Dashboard Articles
# ---------------------------------------------------------

@router.get("/latest")
def latest_dashboard(db: Session = Depends(get_db)):

    articles = (
        db.query(Intelligence)
        .order_by(
            Intelligence.dashboard_score.desc(),
            Intelligence.published_at.desc()
        )
        .limit(20)
        .all()
    )

    return articles


# ---------------------------------------------------------
# Dashboard Stats
# ---------------------------------------------------------

@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db)):

    total = db.query(Intelligence).count()

    critical = db.query(Intelligence).filter(
        Intelligence.priority == "Critical"
    ).count()

    high = db.query(Intelligence).filter(
        Intelligence.priority == "High"
    ).count()

    medium = db.query(Intelligence).filter(
        Intelligence.priority == "Medium"
    ).count()

    low = db.query(Intelligence).filter(
        Intelligence.priority == "Low"
    ).count()

    latest = (
        db.query(Intelligence)
        .order_by(Intelligence.published_at.desc())
        .first()
    )

    return {
        "total_articles": total,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "latest_update": latest.published_at if latest else None
    }


# ---------------------------------------------------------
# Category Distribution
# ---------------------------------------------------------

@router.get("/categories")
def categories(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Intelligence.category,
            func.count(Intelligence.id)
        )
        .group_by(Intelligence.category)
        .all()
    )

    return [
        {
            "category": category,
            "count": count
        }
        for category, count in rows
    ]


# ---------------------------------------------------------
# Country Distribution
# ---------------------------------------------------------

@router.get("/countries")
def countries(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Intelligence.country,
            func.count(Intelligence.id)
        )
        .group_by(Intelligence.country)
        .all()
    )

    return [
        {
            "country": country,
            "count": count
        }
        for country, count in rows
    ]


# ---------------------------------------------------------
# Company Mentions
# ---------------------------------------------------------

@router.get("/companies")
def companies(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Intelligence.company,
            func.count(Intelligence.id)
        )
        .group_by(Intelligence.company)
        .order_by(func.count(Intelligence.id).desc())
        .limit(20)
        .all()
    )

    return [
        {
            "company": company,
            "mentions": count
        }
        for company, count in rows
    ]