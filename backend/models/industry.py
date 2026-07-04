from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Industry(Base):

    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    slug = Column(String(100), unique=True, nullable=False)

    search_query = Column(Text, nullable=False)

    description = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
