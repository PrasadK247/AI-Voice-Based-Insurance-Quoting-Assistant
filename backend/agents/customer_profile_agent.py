"""
UC189 - Customer Profile Agent
LangChain agent for building and managing customer profiles from conversations.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional

from config import get_settings
from utils.logger import setup_logger

settings = get_settings()
logger = setup_logger(__name__)


def _extract_age_func(text: str) -> str:
    """Extract age information from customer text."""
    age_patterns = [
        r"(\d{1,3})\s*(?:years?\s*old|yo|yrs)",
        r"age\s*(?:is\s*)?(\d{1,3})",
        r"i(?:'m| am)\s*(\d{1,3})",
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text.lower())
        if match:
            age = int(match.group(1))
            if 18 <= age <= 120:
                return str(age)
    return "unknown"


def _extract_family_size_func(text: str) -> str:
    """Extract family size from customer text."""
    patterns = [
        r"family\s*of\s*(\d+)",
        r"(\d+)\s*(?:family\s*)?members?",
        r"(\d+)\s*(?:kids?|children)",
        r"(\d+)\s*dependents?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1)
    return "1"


def _assess_risk_factors_func(profile_json: str) -> str:
    """Assess risk factors from profile data."""
    try:
        profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
    except Exception:
        return "Unable to parse profile data."

    factors = []
    age = profile.get("age", 0)
    if age > 50:
        factors.append("age_risk")
    if profile.get("smoking_status"):
        factors.append("smoker_risk")
    if profile.get("pre_existing_conditions"):
        factors.append("medical_history_risk")
    if not factors:
        factors.append("no_significant_risk_factors")
    return ", ".join(factors)


class CustomerProfileAgent:
    """Agent for creating and managing customer profiles."""

    def __init__(self):
        self.agent_executor = self._create_agent()

    def _create_agent(self) -> Optional[Any]:
        """Create the LangChain agent with tools if Azure OpenAI is configured."""
        if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
            return None

        try:
            from langchain_openai import AzureChatOpenAI
            from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
            from langchain.agents import AgentExecutor, create_openai_functions_agent
            from langchain.tools import tool

            llm = AzureChatOpenAI(
                azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                temperature=0.3,
            )

            @tool
            def extract_age(text: str) -> str:
                """Extract age information from customer text."""
                return _extract_age_func(text)

            @tool
            def extract_family_size(text: str) -> str:
                """Extract family size from customer text."""
                return _extract_family_size_func(text)

            @tool
            def assess_risk_factors(profile_json: str) -> str:
                """Assess risk factors from profile data."""
                return _assess_risk_factors_func(profile_json)

            tools = [extract_age, extract_family_size, assess_risk_factors]

            prompt = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            agent = create_openai_functions_agent(llm, tools, prompt)
            return AgentExecutor(agent=agent, tools=tools, verbose=False)
        except Exception as e:
            logger.warning(f"Agent creation failed (likely missing Azure OpenAI credentials): {e}")
            return None

    def _get_system_prompt(self) -> str:
        """Load the system prompt for customer profiling."""
        prompt_paths = ["prompts/profiling_prompt.txt", "backend/prompts/profiling_prompt.txt"]
        for p in prompt_paths:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
        return "You are an AI Insurance Customer Profiling Assistant. Extract key customer attributes and assess risk factors."

    async def create_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create and enrich a customer profile."""
        logger.info(f"Processing profile creation for: {profile_data.get('name')}")
        risk_summary = _assess_risk_factors_func(profile_data)
        return {
            "status": "success",
            "risk_summary": risk_summary,
            "processed_profile": profile_data,
        }

    async def extract_from_transcript(self, transcript: str) -> Dict[str, Any]:
        """Extract customer profile entities directly from voice transcript."""
        logger.info(f"Extracting profile from transcript: '{transcript[:50]}...'")

        # Use LangChain agent if available
        if self.agent_executor:
            try:
                response = await self.agent_executor.ainvoke({"input": transcript})
                output_text = response.get("output", "")
                logger.info(f"LangChain agent profiling output: {output_text}")
            except Exception as e:
                logger.warning(f"LangChain profiling invoke failed: {e}")

        # Robust NLP extraction heuristic
        age_str = _extract_age_func(transcript)
        age = int(age_str) if age_str.isdigit() else 35
        family_size = int(_extract_family_size_func(transcript))

        t = transcript.lower()
        smoker = any(w in t for w in ["smoke", "smoker", "smoking", "tobacco", "cigarette"])
        
        # Medical conditions
        conditions = []
        for cond in ["asthma", "diabetes", "hypertension", "heart disease", "allergies", "cancer", "arthritis"]:
            if cond in t:
                conditions.append(cond)

        # Insurance type
        insurance_type = "health"
        if "life" in t:
            insurance_type = "life"
        elif "auto" in t or "car" in t or "vehicle" in t:
            insurance_type = "auto"
        elif "home" in t or "property" in t or "house" in t:
            insurance_type = "home"

        # Missing fields detection
        missing = []
        if age_str == "unknown":
            missing.append("age")
        if "income" not in t and "salary" not in t and "make" not in t:
            missing.append("annual_income")

        return {
            "name": "Customer",
            "age": age,
            "family_members": family_size,
            "smoking_status": smoker,
            "pre_existing_conditions": conditions,
            "insurance_type": insurance_type,
            "annual_income": 95000.0,
            "missing_fields": missing,
        }
