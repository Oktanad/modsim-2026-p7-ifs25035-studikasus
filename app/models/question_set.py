from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.extensions import Base

class QuestionSet(Base):
    __tablename__ = "question_sets"

    id = Column(Integer, primary_key=True)
    subject = Column(String(100))
    topic = Column(String(200))
    difficulty = Column(String(20))  # mudah / sedang / sulit
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
