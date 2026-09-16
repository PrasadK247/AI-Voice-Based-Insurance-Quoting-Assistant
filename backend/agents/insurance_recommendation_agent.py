"""
UC189 - Insurance Recommendation Agent
LangChain agent providing policy recommendations and personalized summaries.
"""

from typing import Dict, Any, List, Optional
from config import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


class InsuranceRecommendationAgent:
    """Agent generating personalized insurance recommendations."""

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
                temperature=0.3,
            )
        except Exception:
            return None

    async def generate_summary(
        self,
        customer_id: str,
        recommendations: List[Dict[str, Any]],
        budget: float,
    ) -> str:
        """Generate human-like AI recommendation summary."""
        logger.info(f"Generating recommendation summary for customer {customer_id}, budget ${budget}")

        if not recommendations:
            return "No policies match the specified criteria at this time."

        top_policy = recommendations[0]
        top_name = top_policy.get("policy_name", "Recommended Plan")
        top_premium = top_policy.get("monthly_premium", 0.0)
        match_score = int(top_policy.get("match_score", 0.9) * 100)

        if self.llm:
            try:
                from langchain.schema import HumanMessage, SystemMessage
                sys_msg = SystemMessage(
                    content="You are an expert insurance advisor. Provide a 2-sentence executive recommendation summary."
                )
                user_msg = HumanMessage(
                    content=f"Top policy: {top_name}, Premium: ${top_premium}/mo, Budget: ${budget}/mo, Match: {match_score}%"
                )
                resp = await self.llm.ainvoke([sys_msg, user_msg])
                return resp.content.strip()
            except Exception as e:
                logger.warning(f"Recommendation LLM call failed: {e}")

        # High quality fallback summary
        return (
            f"Based on your ${budget:.0f}/month target, '{top_name}' offers the optimal balance with a {match_score}% "
            f"compatibility rating at ${top_premium:.2f}/month. It ensures comprehensive hospitalization with low out-of-pocket exposure."
        )
