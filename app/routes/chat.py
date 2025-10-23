import json
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models import ChatMessage, Session

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
    await manager.connect(websocket, session_id)

    db: AsyncSession = AsyncSessionLocal()

    try:
        # Check if session exists, create if not
        result = await db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            session = Session(session_id=session_id)
            db.add(session)
            await db.commit()

        # Send welcome message
        await manager.send_message(
            json.dumps(
                {
                    "type": "system",
                    "message": "Connected to Lush Moments Chat",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            session_id,
        )

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Save message to database
            chat_message = ChatMessage(
                session_id=session_id,
                sender_type="user",
                message=message_data.get("message", ""),
                timestamp=datetime.utcnow(),
            )
            db.add(chat_message)
            await db.commit()

            # Echo back to client
            await manager.send_message(
                json.dumps(
                    {
                        "type": "user",
                        "message": message_data.get("message", ""),
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                ),
                session_id,
            )

            # Simple auto-reply (in production, this would be AI or admin)
            auto_reply = ChatMessage(
                session_id=session_id,
                sender_type="bot",
                message="Thank you for your message. An agent will respond shortly.",
                timestamp=datetime.utcnow(),
            )
            db.add(auto_reply)
            await db.commit()

            await manager.send_message(
                json.dumps(
                    {
                        "type": "bot",
                        "message": auto_reply.message,
                        "timestamp": auto_reply.timestamp.isoformat(),
                    }
                ),
                session_id,
            )

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        print(f"Client {session_id} disconnected")

    except Exception as e:
        print(f"Error in websocket: {e}")
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
                    "sender_type": msg.sender_type,
                    "message": msg.message,
                    "timestamp": msg.timestamp.isoformat(),
                }
                for msg in messages
            ],
        }
    finally:
        await db.close()
