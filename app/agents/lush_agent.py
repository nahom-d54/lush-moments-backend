"""
Lush Moments AI Agent powered by LangChain and Google Gemini
Handles customer inquiries about packages, themes, gallery, and bookings
"""

import logging
import os
import re

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.prompts import SYSTEM_MESSAGE
from app.agents.tools import TOOLS, _db_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptInjectionFilter:
    def __init__(self):
        self.dangerous_patterns = [
            r"ignore\s+(all\s+)?previous\s+instructions?",
            r"you\s+are\s+now\s+(in\s+)?developer\s+mode",
            r"system\s+override",
            r"reveal\s+prompt",
        ]

        # Fuzzy matching for typoglycemia attacks
        self.fuzzy_patterns = [
            "ignore",
            "bypass",
            "override",
            "reveal",
            "delete",
            "system",
        ]

    def detect_injection(self, text: str) -> bool:
        # Standard pattern matching
        if any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.dangerous_patterns
        ):
            return True

        # Fuzzy matching for misspelled words (typoglycemia defense)
        words = re.findall(r"\b\w+\b", text.lower())
        for word in words:
            for pattern in self.fuzzy_patterns:
                if self._is_similar_word(word, pattern):
                    return True
        return False

    def _is_similar_word(self, word: str, target: str) -> bool:
        """Check if word is a typoglycemia variant of target"""
        if len(word) != len(target) or len(word) < 3:
            return False
        # Same first and last letter, scrambled middle
        return (
            word[0] == target[0]
            and word[-1] == target[-1]
            and sorted(word[1:-1]) == sorted(target[1:-1])
        )

    def sanitize_input(self, text: str) -> str:
        # Normalize common obfuscations
        text = re.sub(r"\s+", " ", text)  # Collapse whitespace
        text = re.sub(r"(.)\1{3,}", r"\1", text)  # Remove char repetition

        for pattern in self.dangerous_patterns:
            text = re.sub(pattern, "[FILTERED]", text, flags=re.IGNORECASE)
        return text[:10000]  # Limit length


class OutputValidator:
    def __init__(self):
        self.suspicious_patterns = [
            r"SYSTEM\s*[:]\s*You\s+are",  # System prompt leakage
            r"API[_\s]KEY[:=]\s*\w+",  # API key exposure
            r"instructions?[:]\s*\d+\.",  # Numbered instructions
        ]

    def validate_output(self, output: str) -> bool:
        return not any(
            re.search(pattern, output, re.IGNORECASE)
            for pattern in self.suspicious_patterns
        )

    def filter_response(self, response: str) -> str:
        if not self.validate_output(response) or len(response) > 5000:
            return "I cannot provide that information for security reasons."
        return response


class HITLController:
    def __init__(self):
        self.high_risk_keywords = [
            "password",
            "api_key",
            "admin",
            "system",
            "bypass",
            "override",
        ]

    def requires_approval(self, user_input: str) -> bool:
        risk_score = sum(
            1 for keyword in self.high_risk_keywords if keyword in user_input.lower()
        )

        injection_patterns = ["ignore instructions", "developer mode", "reveal prompt"]
        risk_score += sum(
            2 for pattern in injection_patterns if pattern in user_input.lower()
        )

        return risk_score >= 3


class SecureLangChainPipeline:
    def __init__(self):
        self.security_filter = PromptInjectionFilter()

    def secure_generate(self, user_input: str) -> str:
        if self.security_filter.detect_injection(user_input):
            return "I cannot process that request."

        clean_input = self.security_filter.sanitize_input(user_input)

        return HumanMessage(content=clean_input)


# Initialize the LLM
def get_llm():
    """Get the Google Gemini LLM instance"""
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.5-flash-lite")

    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable not set")
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    try:
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=1024,
        )
        logger.info(f"Successfully initialized Gemini model: {model}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {str(e)}")
        raise


# Create agent with tools
try:
    llm = get_llm()
    agent = create_agent(model=llm, tools=TOOLS, system_prompt=SYSTEM_MESSAGE)
    logger.info("Agent created successfully")
except Exception as e:
    logger.error(f"Failed to create agent: {str(e)}")
    agent = None


async def run_agent(message: str, db_session: AsyncSession, history=None) -> AIMessage:
    """
    Single-turn agent runner with automatic tool execution via LangGraph.

    Args:
        message: The user's message
        db_session: Database session for tool access
        history: Previous messages in the conversation

    Returns:
        AIMessage with the agent's response
    """
    try:
        # Set the database session in context for tools to access
        _db_session.set(db_session)

        pipeline = SecureLangChainPipeline()

        if agent is None:
            logger.error("Agent not initialized, attempting to recreate")
            temp_llm = get_llm()
            temp_agent = create_agent(
                model=temp_llm, tools=TOOLS, system_prompt=SYSTEM_MESSAGE
            )
            result = await temp_agent.ainvoke(
                {"messages": (history or []) + [pipeline.secure_generate(message)]},
                config={"recursion_limit": 50},
            )
            return result["messages"][-1]

        # Run agent with history
        result = await agent.ainvoke(
            {"messages": (history or []) + [pipeline.secure_generate(message)]},
            config={"recursion_limit": 50},
        )

        # Return the last AI message
        return result["messages"][-1]

    except ValueError as ve:
        # API key or configuration errors
        logger.error(f"Configuration error: {str(ve)}")
        return AIMessage(
            content="I'm having trouble connecting to my AI system. Please contact support or try speaking with a human agent."
        )
    except Exception as e:
        # General errors
        logger.error(f"Agent error: {str(e)}", exc_info=True)
        return AIMessage(
            content="I apologize, but I'm having trouble processing your request right now. Would you like to speak with a human agent instead?"
        )
