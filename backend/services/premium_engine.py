"""
UC189 - Actuarial Premium Calculation Engine
Computes risk-adjusted insurance premiums for Health, Life, Auto, and Home policies.
"""

from typing import Dict, Any, List, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PremiumEngine:
    """Actuarial premium computation engine."""

    # Base rate per $100,000 coverage
    BASE_RATES = {
        "health": 60.0,
        "life": 45.0,
        "auto": 75.0,
        "home": 35.0,
    }

    ADD_ON_RATES = {
        "dental": 25.0,
        "vision": 15.0,
        "maternity": 40.0,
        "critical_illness": 35.0,
        "roadside_assistance": 12.0,
        "zero_depreciation": 30.0,
    }

    def calculate_premium(
        self,
        insurance_type: str,
        coverage_amount: float,
        deductible: float = 500.0,
        term_years: int = 1,
        add_ons: Optional[List[str]] = None,
        customer_id: Optional[str] = None,
        risk_score: float = 0.25,
    ) -> Dict[str, Any]:
        """
        Calculate customized monthly and annual premium breakdown.
        """
        logger.info(
            f"Calculating premium for {insurance_type}, coverage: ${coverage_amount:,.2f}, deductible: ${deductible}"
        )

        add_ons = add_ons or []
        ins_type = insurance_type.lower()
        base_rate = self.BASE_RATES.get(ins_type, 50.0)

        # 1. Base Coverage Factor
        coverage_units = coverage_amount / 100000.0
        calculated_base = base_rate * coverage_units

        # 2. Deductible Discount (Higher deductible = lower premium)
        # $500 deductible is baseline (1.0). Every $500 above lowers premium by 4%, down to 0.75
        deductible_factor = max(0.75, 1.0 - ((deductible - 500.0) / 500.0) * 0.04)

        # 3. Risk Adjustment Factor (from customer profile)
        # risk_score between 0.0 and 1.0; 0.25 is normal baseline (1.0x), 0.8 is 1.55x
        risk_multiplier = 0.85 + (risk_score * 0.9)

        # 4. Term Adjustment
        term_discount = 0.02 * min(term_years - 1, 5)  # up to 10% discount for multi-year
        term_factor = max(0.90, 1.0 - term_discount)

        # 5. Add-on costs
        add_on_total = sum(self.ADD_ON_RATES.get(addon.lower(), 20.0) for addon in add_ons)

        # Final monthly premium calculation
        monthly_premium = (calculated_base * deductible_factor * risk_multiplier * term_factor) + add_on_total
        monthly_premium = max(monthly_premium, 45.0)  # Floor

        # Annual premium with 5% full-payment discount
        annual_premium = monthly_premium * 12 * 0.95

        # Determine appropriate tier label
        if monthly_premium > 500:
            policy_name = f"Executive {ins_type.capitalize()} Elite"
        elif monthly_premium > 350:
            policy_name = f"Premium {ins_type.capitalize()} Shield"
        elif monthly_premium > 200:
            policy_name = f"Comprehensive {ins_type.capitalize()} Care"
        else:
            policy_name = f"Essential {ins_type.capitalize()} Basic"

        return {
            "policy_name": policy_name,
            "insurance_type": ins_type,
            "monthly_premium": round(monthly_premium, 2),
            "annual_premium": round(annual_premium, 2),
            "base_monthly": round(calculated_base, 2),
            "deductible": deductible,
            "risk_multiplier": round(risk_multiplier, 2),
            "add_on_costs": round(add_on_total, 2),
            "savings_annual": round((monthly_premium * 12) - annual_premium, 2),
        }
