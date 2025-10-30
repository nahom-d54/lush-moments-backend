import json
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.lush_agent import run_agent
from app.database import AsyncSessionLocal, get_db
from app.models import ChatMessage, Session
from app.utils.auth import get_current_user

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    # Accept the WebSocket connection first (before any other operations)
    # This is required for CORS to work properly
    await websocket.accept()

    db: AsyncSession = AsyncSessionLocal()

    try:
        # Add connection to manager after accepting
        manager.active_connections[session_id] = websocket

        # Check if session exists, create if not
        result = await db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            session = Session(
                session_id=session_id,
                is_handled_by_agent=True,
                transferred_to_human=False,
            )
            db.add(session)
            await db.commit()
            await db.refresh(session)
        else:
            # Refresh to ensure all attributes are loaded
            await db.refresh(session)

        # Send welcome message
        welcome_msg = "Hello! Welcome to Lush Moments. I'm your AI assistant. How can I help you plan your perfect celebration today?"
        now = datetime.utcnow()

        welcome_chat_msg = ChatMessage(
            session_id=session_id,
            sender_type="bot",
            message=welcome_msg,
            timestamp=now,
        )
        db.add(welcome_chat_msg)
        await db.commit()

        await manager.send_message(
            json.dumps(
                {
                    "type": "bot",
                    "message": welcome_msg,
                    "timestamp": now.isoformat(),
                    "is_agent": True,
                }
            ),
            session_id,
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
                now = datetime.utcnow()

                transfer_chat_msg = ChatMessage(
                    session_id=session_id,
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
                    session_id,
                )
                continue

            # Save user message to database
            now = datetime.utcnow()
            chat_message = ChatMessage(
                session_id=session_id,
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
                session_id,
            )

            # Check if session is handled by agent or transferred to human
            if session.transferred_to_human:
                # Don't send to agent, wait for human response
                now = datetime.utcnow()
                waiting_msg = ChatMessage(
                    session_id=session_id,
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
                    session_id,
                )
            else:
                # Get chat history for context
                history_result = await db.execute(
                    select(ChatMessage)
                    .where(ChatMessage.session_id == session_id)
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
                now = datetime.utcnow()
                auto_reply = ChatMessage(
                    session_id=session_id,
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
                    session_id,
                )

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        print(f"Client {session_id} disconnected")

    except Exception as e:
        print(f"Error in websocket: {e}")
        import traceback

        traceback.print_exc()
        manager.disconnect(session_id)

    finally:
        await db.close()


@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    db: AsyncSession = AsyncSessionLocal()

    try:
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp)
        )
        messages = result.scalars().all()

        return {
            "session_id": session_id,
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
    finally:
        await db.close()


class MergeSessionRequest(BaseModel):
    """Request to merge anonymous chat session with user account"""

    anonymous_session_id: str


@router.post("/chat/merge-session")
async def merge_chat_session(
    request: MergeSessionRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Merge an anonymous chat session with the authenticated user's account.
    Called after login/registration to associate chat history with the user.
    """
    try:
        # Get the anonymous session
        result = await db.execute(
            select(Session).where(Session.session_id == request.anonymous_session_id)
        )
        anonymous_session = result.scalar_one_or_none()

        if not anonymous_session:
            # Session doesn't exist, create a new one linked to the user
            new_session = Session(
                session_id=request.anonymous_session_id, linked_user_id=current_user.id
            )
            db.add(new_session)
            await db.commit()

            return {
                "success": True,
                "message": "New session created and linked to your account",
                "session_id": request.anonymous_session_id,
            }

        # Check if session is already linked to this user
        if anonymous_session.linked_user_id == current_user.id:
            return {
                "success": True,
                "message": "Session already linked to your account",
                "session_id": request.anonymous_session_id,
            }

        # Check if session is linked to a different user
        if anonymous_session.linked_user_id is not None:
            raise HTTPException(
                status_code=400,
                detail="This chat session is already linked to another account",
            )

        # Link the anonymous session to the current user
        anonymous_session.linked_user_id = current_user.id
        await db.commit()

        # Get message count
        result = await db.execute(
            select(ChatMessage).where(
                ChatMessage.session_id == request.anonymous_session_id
            )
        )
        messages = result.scalars().all()

        return {
            "success": True,
            "message": f"Successfully linked chat session with {len(messages)} messages to your account",
            "session_id": request.anonymous_session_id,
            "message_count": len(messages),
        }

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to merge chat session: {str(e)}"
        )


@router.get("/chat/my-sessions")
async def get_user_sessions(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get all chat sessions linked to the authenticated user"""
    result = await db.execute(
        select(Session).where(Session.linked_user_id == current_user.id)
    )
    sessions = result.scalars().all()

    session_list = []
    for session in sessions:
        # Get message count
        msg_result = await db.execute(
            select(ChatMessage).where(ChatMessage.session_id == session.session_id)
        )
        messages = msg_result.scalars().all()

        # Get last message
        last_message = messages[-1] if messages else None

        session_list.append(
            {
                "session_id": session.session_id,
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
        )

    return {"sessions": session_list, "total": len(session_list)}


@router.get("/chat/session/{session_id}/status")
async def get_session_status(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get the status of a chat session (agent vs human)"""
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.session_id,
        "is_handled_by_agent": session.is_handled_by_agent,
        "transferred_to_human": session.transferred_to_human,
        "transfer_reason": session.transfer_reason,
        "created_at": session.created_at.isoformat(),
    }
