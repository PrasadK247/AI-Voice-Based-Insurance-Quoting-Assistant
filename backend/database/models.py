"""
UC189 - Database Models
SQLAlchemy ORM models for customers, policies, quotes, and interactions.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(32), nullable=True)
    occupation = Column(String(128), nullable=True)
    annual_income = Column(Float, nullable=False, default=0.0)
    location = Column(String(128), nullable=True)
    smoking_status = Column(Boolean, default=False)
    pre_existing_conditions = Column(JSON, default=list)
    family_members = Column(Integer, default=1)
    insurance_type = Column(String(64), default="health")
    risk_score = Column(Float, default=0.2)
    risk_category = Column(String(32), default="low")
    created_at = Column(DateTime, default=datetime.utcnow)

    quotes = relationship("Quote", back_populates="customer")
    interactions = relationship("VoiceInteraction", back_populates="customer")


class Policy(Base):
    __tablename__ = "policies"

    policy_id = Column(String(64), primary_key=True, index=True)
    policy_name = Column(String(128), nullable=False)
    provider = Column(String(128), nullable=False)
    tier = Column(String(64), default="standard")  # basic, standard, family, premium, elite
    insurance_type = Column(String(64), default="health")
    base_premium = Column(Float, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    deductible = Column(Float, default=500.0)
    key_benefits = Column(JSON, default=list)
    limitations = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Quote(Base):
    __tablename__ = "quotes"

    quote_id = Column(String(64), primary_key=True, index=True)
    customer_id = Column(String(64), ForeignKey("customers.customer_id"), nullable=True)
    policy_id = Column(String(64), ForeignKey("policies.policy_id"), nullable=True)
    policy_name = Column(String(128), nullable=False)
    insurance_type = Column(String(64), nullable=False)
    monthly_premium = Column(Float, nullable=False)
    annual_premium = Column(Float, nullable=False)
    coverage_amount = Column(Float, nullable=False)
    deductible = Column(Float, nullable=False, default=500.0)
    term_years = Column(Integer, default=1)
    coverage_details = Column(JSON, default=list)
    add_ons = Column(JSON, default=list)
    status = Column(String(32), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="quotes")


class VoiceInteraction(Base):
    __tablename__ = "voice_interactions"

    interaction_id = Column(String(64), primary_key=True, index=True)
    session_id = Column(String(128), nullable=False, index=True)
    customer_id = Column(String(64), ForeignKey("customers.customer_id"), nullable=True)
    user_message = Column(Text, nullable=False)
    assistant_message = Column(Text, nullable=False)
    intent = Column(String(64), default="general_inquiry")
    sentiment = Column(String(32), default="neutral")
    sentiment_score = Column(Float, default=0.5)
    duration_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="interactions")
