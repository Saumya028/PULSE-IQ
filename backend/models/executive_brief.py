from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base


class ExecutiveBrief(Base):

    __tablename__ = "executive_briefs"

    id = Column(Integer, primary_key=True)

    industry = Column(String(100), index=True)

    headline = Column(Text)

    summary = Column(Text)

    key_trends = Column(Text)

    recommended_actions = Column(Text)

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )