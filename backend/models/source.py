from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Source(Base):

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)

    name = Column(String(150), unique=True, nullable=False)

    url = Column(String(300))

    type = Column(String(50))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    