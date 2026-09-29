from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float
)

from sqlalchemy.sql import func

from app.database.database import Base


class Paper(Base):

    __tablename__ = "papers"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # File information

    file_id = Column(
        String,
        nullable=True
    )


    file_hash = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )


    filename = Column(
        String,
        nullable=True
    )


    title = Column(
        String,
        nullable=True
    )


    # Paper statistics

    page_count = Column(
        Integer,
        nullable=True
    )


    word_count = Column(
        Integer,
        nullable=True
    )


    character_count = Column(
        Integer,
        nullable=True
    )


    # Responsible Metrics

    responsible_metrics_analysis = Column(
        Text,
        nullable=True
    )


    responsible_score = Column(
        Float,
        nullable=True
    )


    responsible_rating = Column(
        String,
        nullable=True
    )


    # Principle Detection

    compliance_score = Column(
        Float,
        nullable=True
    )


    # Research Gap

    novelty_level = Column(
        String,
        nullable=True
    )


    average_similarity = Column(
        Float,
        nullable=True
    )


    # NLP

    nlp_analysis = Column(
        Text,
        nullable=True
    )


    # Bibliometric

    bibliometric_analysis = Column(
        Text,
        nullable=True
    )


    # Principle

    principle_analysis = Column(
        Text,
        nullable=True
    )


    # Research Gap

    research_gap_analysis = Column(
        Text,
        nullable=True
    )


    # Multi-Level Framework

    multi_level_analysis = Column(
        Text,
        nullable=True
    )


    # Created Time

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )