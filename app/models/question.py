from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(Text)
    options = Column(Text)  # JSON string: ["A. ...", "B. ...", "C. ...", "D. ..."]
    answer = Column(String(10))  # e.g. "A"
    set_id = Column(Integer, ForeignKey("question_sets.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
