from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base


class Intelligence(Base):

    __tablename__ = "intelligence"

    id = Column(Integer, primary_key=True, index=True)

    industry = Column(String(100), index=True)

    headline = Column(Text)

    summary = Column(Text)

    company = Column(String(150))

    country = Column(String(100))

    category = Column(String(100))

    priority = Column(String(30))

    business_impact = Column(Text)

    recommended_action = Column(Text)

    dashboard_score = Column(Float)

    confidence = Column(Float)

    source = Column(String(200))

    url = Column(Text, unique=True)

    published_at = Column(String(100))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )