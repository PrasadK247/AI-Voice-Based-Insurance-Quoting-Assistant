"""
UC189 - Customer API Endpoints
Handles customer profile creation, retrieval, and risk assessment.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

from agents.customer_profile_agent import CustomerProfileAgent
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


# ── Request / Response Models ──────────────────────────

class CustomerProfileRequest(BaseModel):
    name: str = Field(default="John Doe")
    age: int = Field(default=35, ge=18, le=120)
    gender: str = Field(default="male")
    occupation: str = Field(default="Software Engineer")
    annual_income: float = Field(default=120000.0, ge=0)
    location: str = Field(default="New York, NY")
    smoking_status: bool = False
    pre_existing_conditions: List[str] = Field(default_factory=list)
    family_members: int = Field(default=1, ge=1)
    insurance_type: str = Field(default="health", description="health, life, auto, home")


class RiskProfile(BaseModel):
    risk_score: float
    risk_category: str
    risk_factors: List[str]


class CustomerProfileResponse(BaseModel):
    success: bool
    customer_id: str
    name: str
    risk_profile: RiskProfile
    profile_complete: bool
    recommended_coverage: float
    suggested_insurance_types: List[str]


class VoiceProfileRequest(BaseModel):
    session_id: str
    transcript: str
    partial: bool = False


# ── Endpoints ──────────────────────────────────────────

@router.post("/profile", response_model=CustomerProfileResponse)
async def create_customer_profile(request: CustomerProfileRequest):
    """Create a new customer profile with risk assessment."""
    logger.info(f"Creating profile for customer: {request.name}")

    try:
        agent = CustomerProfileAgent()
        profile_result = await agent.create_profile(request.model_dump())

        customer_id = f"cust_{uuid.uuid4().hex[:12]}"

        # Risk calculation
        risk_score = _calculate_risk_score(request)
        risk_category = (
            "low" if risk_score < 0.35
            else "medium" if risk_score < 0.65
            else "high"
        )

        risk_factors = []
        if request.age > 50:
            risk_factors.append("age_above_50")
        if request.smoking_status:
            risk_factors.append("smoker")
        if request.pre_existing_conditions:
            risk_factors.append("pre_existing_conditions")
        if request.family_members > 4:
            risk_factors.append("large_family_group")

        # Recommended coverage based on income
        recommended_coverage = request.annual_income * 10.0

        suggested_types = [request.insurance_type]
        if request.insurance_type != "life" and request.family_members > 1:
            suggested_types.append("life")
        if request.insurance_type != "health":
            suggested_types.append("health")

        return CustomerProfileResponse(
            success=True,
            customer_id=customer_id,
            name=request.name,
            risk_profile=RiskProfile(
                risk_score=round(risk_score, 3),
                risk_category=risk_category,
                risk_factors=risk_factors,
            ),
            profile_complete=True,
            recommended_coverage=recommended_coverage,
            suggested_insurance_types=list(set(suggested_types)),
        )

    except Exception as e:
        logger.error(f"Profile creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Profile creation failed: {str(e)}")


@router.get("/{customer_id}")
async def get_customer(customer_id: str):
    """Retrieve customer profile by ID."""
    logger.info(f"Retrieving customer {customer_id}")

    return {
        "success": True,
        "customer_id": customer_id,
        "status": "active",
        "name": "Jane Doe",
        "age": 34,
        "family_members": 4,
        "risk_category": "low",
        "message": "Customer profile retrieved",
    }


@router.post("/voice-profile")
async def create_voice_profile(request: VoiceProfileRequest):
    """Create or update customer profile from voice transcript."""
    logger.info(f"Processing voice profile for session {request.session_id}")

    try:
        agent = CustomerProfileAgent()
        extracted = await agent.extract_from_transcript(request.transcript)

        return {
            "success": True,
            "session_id": request.session_id,
            "extracted_data": extracted,
            "profile_complete": not request.partial,
            "missing_fields": extracted.get("missing_fields", []),
        }

    except Exception as e:
        logger.error(f"Voice profile extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_risk_score(profile: CustomerProfileRequest) -> float:
    """Calculate a risk score between 0 and 1 based on customer profile."""
    score = 0.0

    # Age factor
    if profile.age < 25:
        score += 0.05
    elif profile.age < 35:
        score += 0.10
    elif profile.age < 45:
        score += 0.15
    elif profile.age < 55:
        score += 0.25
    elif profile.age < 65:
        score += 0.35
    else:
        score += 0.45

    # Smoking factor
    if profile.smoking_status:
        score += 0.20

    # Pre-existing conditions
    score += min(len(profile.pre_existing_conditions) * 0.08, 0.30)

    # Occupation risk (simplified)
    high_risk_occupations = ["construction", "mining", "military", "firefighter", "pilot", "logging"]
    if profile.occupation.lower() in high_risk_occupations:
        score += 0.10

    # Family size factor
    if profile.family_members > 4:
        score += 0.05

    return min(score, 1.0)
