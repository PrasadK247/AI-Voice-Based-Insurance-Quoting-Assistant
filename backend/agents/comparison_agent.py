"""
UC189 - Policy Comparison Agent
LangChain agent for side-by-side analysis of insurance policies.
"""

from typing import Dict, Any, List, Optional
from config import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)

CATALOG = {
    "pol_001": {
        "policy_id": "pol_001",
        "policy_name": "Premium Health Shield",
        "provider": "HealthGuard Insurance",
        "tier": "premium",
        "monthly_premium": 450.0,
        "coverage_amount": 500000.0,
        "deductible": 500.0,
        "key_benefits": ["Comprehensive hospitalization", "Dental & vision included", "Global coverage", "Zero deductible option"],
        "limitations": ["12-month waiting period for pre-existing conditions"],
    },
    "pol_002": {
        "policy_id": "pol_002",
        "policy_name": "Essential Health Plan",
        "provider": "SafeLife Insurance",
        "tier": "standard",
        "monthly_premium": 250.0,
        "coverage_amount": 300000.0,
        "deductible": 1000.0,
        "key_benefits": ["In-patient coverage", "Emergency services", "Prescription coverage", "Preventive care"],
        "limitations": ["No dental", "No vision", "Network restricted"],
    },
    "pol_003": {
        "policy_id": "pol_003",
        "policy_name": "Family Care Plus",
        "provider": "FamilyFirst Insurance",
        "tier": "family",
        "monthly_premium": 380.0,
        "coverage_amount": 400000.0,
        "deductible": 750.0,
        "key_benefits": ["Family floater plan", "Maternity coverage", "Child immunization", "Wellness programs"],
        "limitations": ["Co-pay required for specialist visits"],
    },
    "pol_004": {
        "policy_id": "pol_004",
        "policy_name": "Budget Health Basic",
        "provider": "ValueInsure",
        "tier": "basic",
        "monthly_premium": 150.0,
        "coverage_amount": 150000.0,
        "deductible": 1500.0,
        "key_benefits": ["Basic hospitalization", "Emergency room", "Generic prescriptions"],
        "limitations": ["High deductible", "Limited network", "No dental/vision"],
    },
    "pol_005": {
        "policy_id": "pol_005",
        "policy_name": "Executive Health Elite",
        "provider": "EliteShield Insurance",
        "tier": "elite",
        "monthly_premium": 650.0,
        "coverage_amount": 1000000.0,
        "deductible": 0.0,
        "key_benefits": ["Unlimited hospitalization", "Full dental & vision", "International coverage", "Executive health checks"],
        "limitations": ["Premium pricing"],
    },
}


class ComparisonAgent:
    """Agent comparing policy trade-offs and recommending the best fit."""

    def __init__(self):
        self.llm = self._get_llm()

    def _get_llm(self) -> Optional[Any]:
        if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
            return None
        try:
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                temperature=0.2,
            )
        except Exception:
            return None

    async def compare(self, customer_id: str, policy_ids: List[str]) -> Dict[str, Any]:
        """Compare specified policies side by side."""
        logger.info(f"Comparing policies {policy_ids} for customer {customer_id}")

        selected_policies = [CATALOG[pid] for pid in policy_ids if pid in CATALOG]
        if not selected_policies:
            selected_policies = list(CATALOG.values())[:2]

        # Determine best balanced option
        sorted_by_val = sorted(
            selected_policies,
            key=lambda x: x["coverage_amount"] / max(x["monthly_premium"], 1),
            reverse=True,
        )
        best = sorted_by_val[0]

        recommendation = (
            f"We recommend '{best['policy_name']}' because it provides the strongest value-to-cost ratio with "
            f"${best['coverage_amount']:,.0f} of coverage for ${best['monthly_premium']:.2f}/mo."
        )

        summary = (
            f"Compared {len(selected_policies)} policies. "
            f"Premium ranges from ${min(p['monthly_premium'] for p in selected_policies):.0f}/mo to "
            f"${max(p['monthly_premium'] for p in selected_policies):.0f}/mo. "
            f"Coverage ranges from ${min(p['coverage_amount'] for p in selected_policies):,.0f} to "
            f"${max(p['coverage_amount'] for p in selected_policies):,.0f}."
        )

        return {
            "policies": selected_policies,
            "recommendation": recommendation,
            "summary": summary,
        }
