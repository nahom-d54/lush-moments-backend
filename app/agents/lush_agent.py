"""
Lush Moments AI Agent powered by LangChain and Google Gemini
Handles customer inquiries about packages, themes, gallery, and bookings
"""

import logging
import os

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.prompts import SYSTEM_MESSAGE
from app.agents.tools import TOOLS, _db_session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

        if agent is None:
            logger.error("Agent not initialized, attempting to recreate")
            temp_llm = get_llm()
            temp_agent = create_agent(
                model=temp_llm, tools=TOOLS, system_prompt=SYSTEM_MESSAGE
            )
            result = await temp_agent.ainvoke(
                {"messages": (history or []) + [HumanMessage(content=message)]},
                config={"recursion_limit": 50},
            )
            return result["messages"][-1]

        # Run agent with history
        result = await agent.ainvoke(
            {"messages": (history or []) + [HumanMessage(content=message)]},
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
