from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, Date, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base


class Elder(Base):
    """
    Elderly information table
    """
    __tablename__ = "elders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Enum("M", "F"), nullable=False)
    care_level = Column(Enum("1", "2", "3", "4", "5"), nullable=False)
    contact_info = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationships
    records = relationship("Record", back_populates="elder")
    keyword_preferences = relationship("KeywordPreference", back_populates="elder")
    answers = relationship("Answer", back_populates="elder")


class Record(Base):
    """
    Record table
    """
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    elder_id = Column(Integer, ForeignKey("elders.id"), nullable=False)

    # Relationships
    elder = relationship("Elder", back_populates="records")
    images = relationship("Image", back_populates="record")
    record_questions = relationship("RecordQuestion", back_populates="record")


class Image(Base):
    """
    Image table for storing URLs associated with records
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False)
    url = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationships
    record = relationship("Record", back_populates="images")


class Keyword(Base):
    """
    Keywords table
    """
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")


class KeywordPreference(Base):
    """
    Keyword preferences table for elders
    """
    __tablename__ = "keyword_preferences"

    id = Column(Integer, primary_key=True, index=True)
    elder_id = Column(Integer, ForeignKey("elders.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id"), nullable=False)
    is_preferred = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationships
    elder = relationship("Elder", back_populates="keyword_preferences")


class Question(Base):
    """
    Questions table
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")


class RecordQuestion(Base):
    """
    Table linking records and questions
    """
    __tablename__ = "record_questions"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("records.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationships
    record = relationship("Record", back_populates="record_questions")


class Answer(Base):
    """
    Answers table for storing responses to questions
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    elder_id = Column(Integer, ForeignKey("elders.id"), nullable=False)
    response = Column(Text, nullable=False)
    response_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    # Relationships
    elder = relationship("Elder", back_populates="answers")


class ActivityGuide(Base):
    """
    Activity guides (lesson plans) table
    """
    __tablename__ = "activity_guides"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")


class GuideQuestion(Base):
    """
    Table linking activity guides and questions
    """
    __tablename__ = "guide_questions"

    id = Column(Integer, primary_key=True, index=True)
    guide_id = Column(Integer, ForeignKey("activity_guides.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")