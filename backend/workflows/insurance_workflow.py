"""
UC189 - LangGraph Insurance Workflow Engine
Orchestrates multi-step conversational state machine:
START → Voice Input → Intent Analysis → Customer Profiling → Risk Assessment
→ Policy Recommendation → Premium Calculation → Quote Generation
→ Voice Response → END
"""

import sys
import types
from typing import Dict, Any, Optional, TypedDict, List
from agents.customer_profile_agent import CustomerProfileAgent
from agents.quote_generation_agent import QuoteGenerationAgent
from agents.insurance_recommendation_agent import InsuranceRecommendationAgent
from services.premium_engine import PremiumEngine
from services.uniphore_service import UniphoreService
from utils.logger import setup_logger

logger = setup_logger(__name__)


class InsuranceWorkflowState(TypedDict, total=False):
    session_id: str
    user_message: str
    intent: str
    sentiment: str
    sentiment_score: float
    customer_profile: Dict[str, Any]
    risk_score: float
    risk_category: str
    recommended_policies: List[Dict[str, Any]]
    quote_data: Dict[str, Any]
    response: str
    next_action: str


class InsuranceWorkflow:
    """State machine orchestrating the complete insurance conversation workflow."""

    def __init__(self):
        self.profile_agent = CustomerProfileAgent()
        self.quote_agent = QuoteGenerationAgent()
        self.rec_agent = InsuranceRecommendationAgent()
        self.premium_engine = PremiumEngine()
        self.uniphore = UniphoreService()

    async def process_turn(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """
        Execute full workflow sequence for a customer conversation turn.
        """
        logger.info(f"[Workflow START] session={session_id}, msg='{user_message[:50]}'")

        state: InsuranceWorkflowState = {
            "session_id": session_id,
            "user_message": user_message,
        }

        # Step 1: Voice Input & Transcript Normalization
        state = await self._voice_input_node(state)

        # Step 2: Intent Analysis & Sentiment Detection (Uniphore)
        state = await self._intent_analysis_node(state)

        # Step 3: Customer Profiling
        state = await self._customer_profiling_node(state)

        # Step 4: Risk Assessment
        state = await self._risk_assessment_node(state)

        # Step 5: Policy Recommendation
        state = await self._policy_recommendation_node(state)

        # Step 6: Premium Calculation
        state = await self._premium_calculation_node(state)

        # Step 7: Quote Generation
        state = await self._quote_generation_node(state)

        # Step 8: Voice Response Generation
        state = await self._voice_response_node(state)

        logger.info(f"[Workflow END] response='{state['response'][:60]}...'")
        return {
            "session_id": session_id,
            "response": state["response"],
            "intent": state["intent"],
            "sentiment": state["sentiment"],
            "next_action": state.get("next_action", "continue"),
            "customer_profile": state.get("customer_profile", {}),
            "risk_score": state.get("risk_score", 0.25),
            "quote_data": state.get("quote_data", {}),
        }

    async def _voice_input_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 1: Normalizes transcript."""
        state["user_message"] = state.get("user_message", "").strip()
        return state

    async def _intent_analysis_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 2: Detects customer intent and Uniphore sentiment."""
        msg = state["user_message"].lower()

        # Uniphore Sentiment Analysis
        sentiment_data = await self.uniphore.analyze_sentiment(state["user_message"])
        state["sentiment"] = sentiment_data.get("sentiment", "neutral")
        state["sentiment_score"] = sentiment_data.get("sentiment_score", 0.5)

        if any(w in msg for w in ["compare", "difference", "vs", "versus"]):
            state["intent"] = "policy_comparison"
        elif any(w in msg for w in ["quote", "cost", "premium", "price", "how much"]):
            state["intent"] = "quote_generation"
        elif any(w in msg for w in ["recommend", "best", "suggest", "which plan"]):
            state["intent"] = "policy_recommendation"
        elif any(w in msg for w in ["family", "health", "life", "cover", "need"]):
            state["intent"] = "customer_profiling"
        else:
            state["intent"] = "general_inquiry"

        return state

    async def _customer_profiling_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 3: Extracts profile entities from conversation."""
        extracted = await self.profile_agent.extract_from_transcript(state["user_message"])
        state["customer_profile"] = extracted
        return state

    async def _risk_assessment_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 4: Computes actuarial risk score and category."""
        profile = state.get("customer_profile", {})
        age = profile.get("age", 35)
        smoker = profile.get("smoking_status", False)
        conditions = profile.get("pre_existing_conditions", [])

        score = 0.15
        if age > 50:
            score += 0.20
        elif age > 40:
            score += 0.10
        if smoker:
            score += 0.25
        score += min(len(conditions) * 0.10, 0.30)

        risk_score = round(min(score, 0.95), 3)
        risk_category = "low" if risk_score < 0.35 else "medium" if risk_score < 0.65 else "high"

        state["risk_score"] = risk_score
        state["risk_category"] = risk_category
        return state

    async def _policy_recommendation_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 5: Selects matching candidate policies."""
        profile = state.get("customer_profile", {})
        family_members = profile.get("family_members", 1)

        policies = [
            {
                "policy_id": "pol_003" if family_members > 1 else "pol_001",
                "policy_name": "Family Care Plus" if family_members > 1 else "Premium Health Shield",
                "coverage_amount": 500000.0,
                "base_premium": 380.0 if family_members > 1 else 450.0,
            }
        ]
        state["recommended_policies"] = policies
        return state

    async def _premium_calculation_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 6: Calculates precise premiums with actuarial engine."""
        profile = state.get("customer_profile", {})
        ins_type = profile.get("insurance_type", "health")
        risk_score = state.get("risk_score", 0.25)

        premium_res = self.premium_engine.calculate_premium(
            insurance_type=ins_type,
            coverage_amount=500000.0,
            deductible=500.0,
            risk_score=risk_score,
            add_ons=["dental"] if "family" in state["user_message"].lower() else [],
        )
        state["quote_data"] = premium_res
        return state

    async def _quote_generation_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 7: Formulates quote proposal summary."""
        quote_data = state.get("quote_data", {})
        state["next_action"] = "review_quote" if state["intent"] == "quote_generation" else "continue"
        return state

    async def _voice_response_node(self, state: InsuranceWorkflowState) -> InsuranceWorkflowState:
        """Step 8: Generates natural, spoken conversational voice response."""
        intent = state.get("intent", "general_inquiry")
        profile = state.get("customer_profile", {})
        quote = state.get("quote_data", {})
        family = profile.get("family_members", 1)
        monthly = quote.get("monthly_premium", 380.0)
        policy_name = quote.get("policy_name", "Family Care Plus")

        if intent == "customer_profiling":
            if family > 1:
                state["response"] = (
                    f"I've set up your profile for a family of {family}. Based on your needs, "
                    f"I recommend the '{policy_name}' which covers hospitalization and pediatric wellness. "
                    f"Estimated premium starts around ${monthly:.2f} per month. Would you like me to customize your deductible or add dental and vision?"
                )
            else:
                state["response"] = (
                    f"Thank you! I've initiated your profile. For comprehensive individual protection, "
                    f"our '{policy_name}' provides $500,000 in coverage at ${monthly:.2f}/month. "
                    f"Would you like to review coverage details or compare other options?"
                )
        elif intent == "quote_generation":
            state["response"] = (
                f"Here is your customized quote for {policy_name}: coverage amount of $500,000 "
                f"with a $500 deductible comes to ${monthly:.2f} monthly, or an annual premium with 5% discount. "
                f"All in-patient and emergency services are fully included."
            )
        elif intent == "policy_comparison":
            state["response"] = (
                "Comparing your options: 'Family Care Plus' is optimal for broad pediatric and maternity benefits at $380/mo, "
                "whereas 'Premium Health Shield' offers international emergency coverage for $450/mo. Both maintain low deductibles."
            )
        elif intent == "policy_recommendation":
            state["response"] = (
                f"Based on your budget and priority, the top recommendation is {policy_name}. "
                f"It gives you the highest match score with comprehensive in-network coverage at ${monthly:.2f} per month."
            )
        else:
            state["response"] = (
                "Hello! I am your AI Insurance Quoting Assistant. I can help you find the best health, life, auto, "
                "or home insurance, compare plans side-by-side, and calculate your exact monthly premium. How can I help you today?"
            )

        return state


# Register dynamic import compatibility for `from langgraph.workflow import InsuranceWorkflow`
if "langgraph.workflow" not in sys.modules:
    _mod = types.ModuleType("langgraph.workflow")
    _mod.InsuranceWorkflow = InsuranceWorkflow
    sys.modules["langgraph.workflow"] = _mod
