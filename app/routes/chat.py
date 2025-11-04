import json
from datetime import datetime, timezone
from typing import Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.lush_agent import run_agent
from app.database import AsyncSessionLocal, get_db
from app.models import ChatMessage, Session, User
from app.utils.auth import get_current_user, verify_token

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
):
    """
    WebSocket chat endpoint. Requires authentication via token in query params.
    Both anonymous and regular users must provide a valid JWT token.
    Expected URL: /ws/chat?token=<jwt_token>
    """
    # Accept the WebSocket connection first (before any other operations)
    # This is required for CORS to work properly
    await websocket.accept()

    db: AsyncSession = AsyncSessionLocal()
    user_id_str = None

    try:
        # Get token from query params
        query_params = dict(websocket.query_params)
        token = query_params.get("token")

        if not token:
            await websocket.send_json(
                {
                    "type": "error",
                    "message": "Missing token in query parameters",
                }
            )
            await websocket.close(code=1008)  # Policy violation
            return

        # Verify token and get user
        user_id_hex = verify_token(token)
        if user_id_hex is None:
            await websocket.send_json(
                {"type": "error", "message": "Invalid or expired token"}
            )
            await websocket.close(code=1008)  # Policy violation
            return

        # Get user by ID (token contains user ID, not email)

        try:
            user_uuid = UUID(hex=user_id_hex)
        except (ValueError, AttributeError):
            await websocket.send_json(
                {"type": "error", "message": "Invalid token format"}
            )
            await websocket.close(code=1008)  # Policy violation
            return

        result = await db.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()

        if user is None:
            await websocket.send_json({"type": "error", "message": "User not found"})
            await websocket.close(code=1008)  # Policy violation
            return

        # Store user_id as string and UUID for later use
        user_id_str = str(user_uuid)
        user_id = user_uuid

        # Add connection to manager after authentication
        manager.active_connections[user_id_str] = websocket

        # Check if user has a session, create if not
        result = await db.execute(select(Session).where(Session.user_id == user_id))
        session = result.scalar_one_or_none()

        if not session:
            session = Session(
                user_id=user_id,
                is_handled_by_agent=True,
                transferred_to_human=False,
            )
            db.add(session)
            await db.commit()
            await db.refresh(session)
        else:
            # Refresh to ensure all attributes are loaded
            await db.refresh(session)

        # Store session_id to avoid lazy loading issues
        session_id = session.id

        # Send welcome message (don't save to database to avoid cluttering chat history)
        welcome_msg = "Hello! Welcome to Lush Moments. I'm your AI assistant. How can I help you plan your perfect celebration today?"
        now = datetime.now(timezone.utc)

        await manager.send_message(
            json.dumps(
                {
                    "type": "bot",
                    "message": welcome_msg,
                    "timestamp": now.isoformat(),
                    "is_agent": True,
                }
            ),
            user_id_str,
        )

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            user_message = message_data.get("message", "")
            message_type = message_data.get("type", "message")

            # Handle "transfer to human" request
            if message_type == "request_human":
                session.transferred_to_human = True
                session.is_handled_by_agent = False
                session.transfer_reason = (
                    user_message or "User requested human assistance"
                )
                await db.commit()
                await db.refresh(session)

                transfer_msg = (
                    "I've transferred you to a human agent. "
                    "One of our team members will be with you shortly!"
                )
                now = datetime.now(timezone.utc)

                transfer_chat_msg = ChatMessage(
                    session_id=session_id,
                    user_id=user_id,
                    sender_type="bot",
                    message=transfer_msg,
                    timestamp=now,
                )
                db.add(transfer_chat_msg)
                await db.commit()

                await manager.send_message(
                    json.dumps(
                        {
                            "type": "system",
                            "message": transfer_msg,
                            "timestamp": now.isoformat(),
                            "transferred": True,
                        }
                    ),
                    user_id_str,
                )
                continue

            # Save user message to database
            now = datetime.now(timezone.utc)
            chat_message = ChatMessage(
                session_id=session_id,
                user_id=user_id,
                sender_type="user",
                message=user_message,
                timestamp=now,
            )
            db.add(chat_message)
            await db.commit()

            # Refresh session to ensure attributes are loaded
            await db.refresh(session)

            # Echo back to client
            await manager.send_message(
                json.dumps(
                    {
                        "type": "user",
                        "message": user_message,
                        "timestamp": now.isoformat(),
                    }
                ),
                user_id_str,
            )

            # Check if session is handled by agent or transferred to human
            if session.transferred_to_human:
                # Don't send to agent, wait for human response
                now = datetime.now(timezone.utc)
                waiting_msg = ChatMessage(
                    session_id=session_id,
                    user_id=user_id,
                    sender_type="bot",
                    message="A human agent will respond to your message shortly...",
                    timestamp=now,
                )
                db.add(waiting_msg)
                await db.commit()

                await manager.send_message(
                    json.dumps(
                        {
                            "type": "bot",
                            "message": waiting_msg.message,
                            "timestamp": now.isoformat(),
                            "is_agent": False,
                        }
                    ),
                    user_id_str,
                )
            else:
                # Get chat history for context
                history_result = await db.execute(
                    select(ChatMessage)
                    .where(ChatMessage.user_id == user_id)
                    .order_by(ChatMessage.timestamp)
                    .limit(20)  # Last 20 messages for context
                )
                history = history_result.scalars().all()

                # Convert to LangChain message format
                from langchain_core.messages import AIMessage, HumanMessage

                chat_history = []
                for msg in history[:-1]:  # Exclude the message we just added
                    if msg.sender_type.value == "user":
                        chat_history.append(HumanMessage(content=msg.message))
                    elif msg.sender_type.value in ["bot", "admin"]:
                        chat_history.append(AIMessage(content=msg.message))

                # Get AI response using the agent
                try:
                    ai_response_message = await run_agent(
                        message=user_message,
                        db_session=db,
                        history=chat_history,
                    )
                    ai_response = ai_response_message.content
                except Exception as e:
                    print(f"Agent error in chat route: {e}")
                    ai_response = (
                        "I apologize, but I'm having trouble right now. "
                        "Would you like to speak with a human agent?"
                    )

                # Save AI response
                now = datetime.now(timezone.utc)
                auto_reply = ChatMessage(
                    session_id=session_id,
                    user_id=user_id,
                    sender_type="bot",
                    message=ai_response,
                    timestamp=now,
                )
                db.add(auto_reply)
                await db.commit()

                await manager.send_message(
                    json.dumps(
                        {
                            "type": "bot",
                            "message": ai_response,
                            "timestamp": now.isoformat(),
                            "is_agent": True,
                        }
                    ),
                    user_id_str,
                )

    except WebSocketDisconnect:
        if user_id_str:
            manager.disconnect(user_id_str)
            print(f"Client {user_id_str} disconnected")

    except Exception as e:
        print(f"Error in websocket: {e}")
        import traceback

        traceback.print_exc()
        if user_id_str:
            manager.disconnect(user_id_str)

    finally:
        await db.close()


@router.get("/chat/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for the authenticated user."""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.timestamp)
    )
    messages = result.scalars().all()

    return {
        "user_id": str(current_user.id),
        "messages": [
            {
                "id": str(msg.id),
                "sender_type": msg.sender_type.value,
                "message": msg.message,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in messages
        ],
    }


@router.get("/chat/session")
async def get_user_session(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get the chat session for the authenticated user"""
    result = await db.execute(select(Session).where(Session.user_id == current_user.id))
    session = result.scalar_one_or_none()

    if not session:
        # Create session if doesn't exist
        session = Session(
            user_id=current_user.id,
            is_handled_by_agent=True,
            transferred_to_human=False,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)

    # Get message count
    msg_result = await db.execute(
        select(ChatMessage).where(ChatMessage.user_id == current_user.id)
    )
    messages = msg_result.scalars().all()

    # Get last message
    last_message = messages[-1] if messages else None

    return {
        "session_id": str(session.id),
        "user_id": str(current_user.id),
        "created_at": session.created_at.isoformat(),
        "message_count": len(messages),
        "is_handled_by_agent": session.is_handled_by_agent,
        "transferred_to_human": session.transferred_to_human,
        "last_message": (
            {
                "sender_type": last_message.sender_type.value,
                "message": last_message.message,
                "timestamp": last_message.timestamp.isoformat(),
            }
            if last_message
            else None
        ),
    }


@router.get("/chat/status")
async def get_session_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the status of the user's chat session (agent vs human). Must be authenticated."""
    result = await db.execute(select(Session).where(Session.user_id == current_user.id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": str(session.id),
        "user_id": str(current_user.id),
        "is_handled_by_agent": session.is_handled_by_agent,
        "transferred_to_human": session.transferred_to_human,
        "transfer_reason": session.transfer_reason,
        "created_at": session.created_at.isoformat(),
    }
