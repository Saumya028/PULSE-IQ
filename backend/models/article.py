from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Article(Base):

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)

    industry_id = Column(
        Integer,
        ForeignKey("industries.id"),
        nullable=False
    )

    source_id = Column(
        Integer,
        ForeignKey("sources.id")
    )

    title = Column(Text, nullable=False)

    description = Column(Text)

    url = Column(Text, unique=True)

    published_at = Column(DateTime)

    content_hash = Column(String(64), unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
