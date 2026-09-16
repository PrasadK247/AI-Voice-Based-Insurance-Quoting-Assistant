"""
UC189 - Recommendation API Endpoints
AI-powered policy recommendations based on customer profile and preferences.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from agents.insurance_recommendation_agent import InsuranceRecommendationAgent
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


# ── Request / Response Models ──────────────────────────

class RecommendationRequest(BaseModel):
    customer_id: str
    budget_monthly: float = Field(default=500.0, gt=0)
    priorities: List[str] = Field(
        default_factory=lambda: ["coverage", "premium", "network"],
        description="Ordered list of priorities",
    )
    insurance_type: Optional[str] = "health"
    exclude_policies: List[str] = Field(default_factory=list)


class PolicyRecommendation(BaseModel):
    rank: int
    policy_id: str
    policy_name: str
    provider: str
    match_score: float
    monthly_premium: float
    annual_premium: float
    coverage_amount: float
    key_benefits: List[str]
    limitations: List[str]
    reasoning: str


class RecommendationResponse(BaseModel):
    success: bool
    customer_id: str
    total_recommendations: int
    recommendations: List[PolicyRecommendation]
    ai_summary: str


# ── Sample Policy Catalog ──────────────────────────────

SAMPLE_POLICIES = [
    {
        "policy_id": "pol_001",
        "policy_name": "Premium Health Shield",
        "provider": "HealthGuard Insurance",
        "base_premium": 450.0,
        "coverage_amount": 500000.0,
        "key_benefits": [
            "Comprehensive hospitalization",
            "Dental & vision included",
            "Global coverage",
            "Zero deductible option",
        ],
        "limitations": ["12-month waiting period for pre-existing conditions"],
        "tier": "premium",
    },
    {
        "policy_id": "pol_002",
        "policy_name": "Essential Health Plan",
        "provider": "SafeLife Insurance",
        "base_premium": 250.0,
        "coverage_amount": 300000.0,
        "key_benefits": [
            "In-patient coverage",
            "Emergency services",
            "Prescription coverage",
            "Preventive care",
        ],
        "limitations": ["No dental", "No vision", "Network restricted"],
        "tier": "standard",
    },
    {
        "policy_id": "pol_003",
        "policy_name": "Family Care Plus",
        "provider": "FamilyFirst Insurance",
        "base_premium": 380.0,
        "coverage_amount": 400000.0,
        "key_benefits": [
            "Family floater plan",
            "Maternity coverage",
            "Child immunization",
            "Wellness programs",
        ],
        "limitations": ["Co-pay required for specialist visits"],
        "tier": "family",
    },
    {
        "policy_id": "pol_004",
        "policy_name": "Budget Health Basic",
        "provider": "ValueInsure",
        "base_premium": 150.0,
        "coverage_amount": 150000.0,
        "key_benefits": [
            "Basic hospitalization",
            "Emergency room",
            "Generic prescriptions",
        ],
        "limitations": [
            "High deductible ($1,500)",
            "Limited network",
            "No dental/vision",
            "Annual caps on benefits",
        ],
        "tier": "basic",
    },
    {
        "policy_id": "pol_005",
        "policy_name": "Executive Health Elite",
        "provider": "EliteShield Insurance",
        "base_premium": 650.0,
        "coverage_amount": 1000000.0,
        "key_benefits": [
            "Unlimited hospitalization",
            "Full dental & vision",
            "International coverage",
            "Executive health checks",
            "Mental health support",
            "Air ambulance",
        ],
        "limitations": ["Premium pricing"],
        "tier": "elite",
    },
]


# ── Endpoints ──────────────────────────────────────────

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get AI-powered insurance policy recommendations."""
    logger.info(f"Generating recommendations for customer {request.customer_id}")

    try:
        agent = InsuranceRecommendationAgent()

        # Filter policies within reasonable range of budget
        eligible_policies = [
            p for p in SAMPLE_POLICIES
            if p["base_premium"] <= request.budget_monthly * 1.3
            and p["policy_id"] not in request.exclude_policies
        ]

        if not eligible_policies:
            eligible_policies = sorted(SAMPLE_POLICIES, key=lambda x: x["base_premium"])[:3]

        # Score and rank policies
        scored = []
        for policy in eligible_policies:
            score = _score_policy(policy, request)
            scored.append((score, policy))

        scored.sort(key=lambda x: x[0], reverse=True)

        recommendations = []
        for rank, (score, policy) in enumerate(scored[:5], start=1):
            recommendations.append(
                PolicyRecommendation(
                    rank=rank,
                    policy_id=policy["policy_id"],
                    policy_name=policy["policy_name"],
                    provider=policy["provider"],
                    match_score=round(score, 2),
                    monthly_premium=policy["base_premium"],
                    annual_premium=round(policy["base_premium"] * 12 * 0.95, 2),
                    coverage_amount=policy["coverage_amount"],
                    key_benefits=policy["key_benefits"],
                    limitations=policy["limitations"],
                    reasoning=_generate_reasoning(policy, request, score),
                )
            )

        # Generate AI summary
        ai_summary = await agent.generate_summary(
            customer_id=request.customer_id,
            recommendations=[r.model_dump() for r in recommendations],
            budget=request.budget_monthly,
        )

        return RecommendationResponse(
            success=True,
            customer_id=request.customer_id,
            total_recommendations=len(recommendations),
            recommendations=recommendations,
            ai_summary=ai_summary,
        )

    except Exception as e:
        logger.error(f"Recommendation generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _score_policy(policy: dict, request: RecommendationRequest) -> float:
    """Score a policy based on customer preferences."""
    score = 0.55  # Base score

    # Budget alignment
    budget_ratio = policy["base_premium"] / request.budget_monthly
    if budget_ratio <= 0.8:
        score += 0.15
    elif budget_ratio <= 1.0:
        score += 0.20
    elif budget_ratio <= 1.1:
        score += 0.10
    else:
        score -= 0.10

    # Priority weighting
    for i, priority in enumerate(request.priorities):
        weight = 0.12 - (i * 0.03)
        if priority == "coverage" and policy["coverage_amount"] >= 400000:
            score += weight
        elif priority == "premium" and policy["base_premium"] <= request.budget_monthly:
            score += weight
        elif priority == "network" and policy["tier"] in ("premium", "elite"):
            score += weight
        elif priority == "benefits" and len(policy["key_benefits"]) >= 4:
            score += weight

    # Tier bonus
    tier_scores = {"elite": 0.08, "premium": 0.07, "family": 0.06, "standard": 0.04, "basic": 0.02}
    score += tier_scores.get(policy["tier"], 0)

    return min(max(score, 0.40), 0.98)


def _generate_reasoning(policy: dict, request: RecommendationRequest, score: float) -> str:
    """Generate human-readable reasoning for a recommendation."""
    reasons = []

    if policy["base_premium"] <= request.budget_monthly:
        reasons.append(f"Fits your monthly budget of ${request.budget_monthly:.0f}")
    else:
        reasons.append("Slightly exceeds target budget but provides exceptional tier protections")

    reasons.append(f"${policy['coverage_amount']:,.0f} overall coverage limit")

    if len(policy["key_benefits"]) >= 4:
        reasons.append("Comprehensive multi-category benefit package")

    if policy["tier"] in ("premium", "elite", "family"):
        reasons.append("Top customer rating and broad hospital network")

    if len(policy["limitations"]) <= 1:
        reasons.append("Low policy restrictions")

    return ". ".join(reasons) + "."
