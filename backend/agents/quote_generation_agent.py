"""
UC189 - Quote Generation Agent
LangChain agent that composes customized insurance quotes and coverage breakdowns.
"""

import os
from typing import Dict, Any, Optional
from config import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


class QuoteGenerationAgent:
    """Agent that creates structured insurance quote presentations."""

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
        except Exception as e:
            logger.warning(f"Failed to initialize AzureChatOpenAI for QuoteAgent: {e}")
            return None

    async def generate(
        self,
        customer_id: str,
        insurance_type: str,
        coverage_amount: float,
        premium_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate tailored quote analysis and narrative."""
        logger.info(f"Generating quote proposal for customer {customer_id} on {insurance_type}")

        policy_name = premium_data.get("policy_name", "Comprehensive Care")
        monthly = premium_data.get("monthly_premium", 350.0)
        annual = premium_data.get("annual_premium", 3990.0)

        # If LLM available, generate a custom explanatory summary
        if self.llm:
            try:
                from langchain.schema import HumanMessage, SystemMessage
                sys_msg = SystemMessage(
                    content="You are an insurance quoting assistant. Briefly explain why this policy and premium fits the customer's requested coverage."
                )
                user_msg = HumanMessage(
                    content=f"Customer ID: {customer_id}, Coverage: ${coverage_amount:,.2f}, Monthly: ${monthly}, Policy: {policy_name}"
                )
                response = await self.llm.ainvoke([sys_msg, user_msg])
                narrative = response.content.strip()
            except Exception as e:
                logger.warning(f"Quote LLM generation failed: {e}")
                narrative = None
        else:
            narrative = None

        if not narrative:
            narrative = (
                f"Your customized {policy_name} provides robust protection with a ${coverage_amount:,.0f} limit "
                f"at an estimated ${monthly:.2f}/month. Paying annually gives you a 5% savings (${annual:.2f}/year)."
            )

        return {
            "customer_id": customer_id,
            "policy_name": policy_name,
            "narrative": narrative,
            "confidence_score": 0.96,
        }
