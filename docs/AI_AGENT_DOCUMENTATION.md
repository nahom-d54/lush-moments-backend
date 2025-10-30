# Lush Moments AI Chat Agent Documentation

## Overview

The Lush Moments AI Chat Agent is an intelligent chatbot powered by **Google Gemini (via LangChain)** and **LangGraph**. It provides 24/7 automated customer support with the ability to transfer to human agents when needed.

## Architecture

### Components

1. **LangChain + Google Gemini**: Core AI language model
2. **LangGraph**: Workflow orchestration for agent behavior
3. **Database Tools**: Real-time access to business data
4. **WebSocket**: Real-time bidirectional communication
5. **Session Management**: Tracks agent vs human handling

### Data Flow

```
User Message (WebSocket)
    ↓
Session Check (Agent or Human?)
    ↓
[IF AGENT] → LangGraph Workflow
    ↓
Tool Selection (get_packages, get_themes, etc.)
    ↓
Database Query
    ↓
AI Response Generation
    ↓
WebSocket → User

[IF HUMAN] → Queue for Human Response
```

## Agent Capabilities

### Knowledge Domains

The AI agent has access to:

1. **Package Information** (`get_packages_info`)
   - Names, descriptions, pricing
   - Features and inclusions
   
2. **Theme Catalog** (`get_themes_info`)
   - Available decoration themes
   - Theme descriptions and styles
   
3. **Gallery Examples** (`get_gallery_items`)
   - Past event photos
   - Categories and descriptions
   
4. **Customer Testimonials** (`get_testimonials`)
   - Client reviews
   - Ratings and event types
   
5. **Booking Process** (`get_booking_info`)
   - How to book
   - Timeline recommendations
   - Requirements
   
6. **FAQ** (`search_faq`)
   - Payment information
   - Delivery and setup
   - Customization options
   - Consultation details

### Conversation Guidelines

The agent is programmed to:

✅ **STAY ON TOPIC**: Only answer questions about Lush Moments services
✅ **USE TOOLS**: Always query database for accurate information
✅ **BE HELPFUL**: Provide specific, detailed answers
✅ **KNOW LIMITS**: Suggest human transfer for complex requests
✅ **NO FABRICATION**: Never make up information
✅ **PROFESSIONAL**: Warm, enthusiastic, professional tone

## Setup Instructions

### 1. Get Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 2. Configure Environment

Add to `.env`:

```bash
GOOGLE_API_KEY=your-google-gemini-api-key-here
```

### 3. Install Dependencies

Already included in `pyproject.toml`:
- `langchain-google-genai>=3.0.0`
- `langchain>=1.0.2`
- `langgraph>=1.0.1`

### 4. Database Migration

```bash
alembic upgrade head
```

This adds the following fields to the `sessions` table:
- `is_handled_by_agent` (Boolean): Currently handled by AI?
- `transferred_to_human` (Boolean): Has been transferred to human?
- `transfer_reason` (Text): Why transferred

## API Endpoints

### WebSocket Chat

**Endpoint**: `ws://localhost:8000/chat/ws/chat/{session_id}`

**Message Format** (Client → Server):

```json
{
  "type": "message",
  "message": "What packages do you offer?"
}
```

**Transfer Request**:

```json
{
  "type": "request_human",
  "message": "User requested human assistance"
}
```

**Message Format** (Server → Client):

```json
{
  "type": "bot",  // or "user", "system"
  "message": "We offer three packages...",
  "timestamp": "2025-10-29T20:00:00",
  "is_agent": true,  // false if human
  "transferred": false  // true when transferred
}
```

### Get Session Status

**Endpoint**: `GET /chat/session/{session_id}/status`

**Response**:

```json
{
  "session_id": "session-123",
  "is_handled_by_agent": true,
  "transferred_to_human": false,
  "transfer_reason": null,
  "created_at": "2025-10-29T19:00:00"
}
```

### Get User Sessions

**Endpoint**: `GET /chat/my-sessions`

**Auth**: Required (Bearer token)

**Response**:

```json
{
  "sessions": [
    {
      "session_id": "session-123",
      "created_at": "2025-10-29T19:00:00",
      "message_count": 8,
      "is_handled_by_agent": false,
      "transferred_to_human": true,
      "last_message": {
        "sender_type": "admin",
        "message": "I'll help you with that!",
        "timestamp": "2025-10-29T20:00:00"
      }
    }
  ],
  "total": 1
}
```

## Frontend Integration

### Features

1. **WebSocket Connection**: Real-time bi-directional chat
2. **Auto-Reconnect**: Handles connection drops
3. **Message Persistence**: Stores messages in real-time
4. **Transfer Button**: "Talk to a Human Agent"
5. **Status Indicators**: Shows AI vs Human, connection status
6. **Visual Feedback**: Different colors for system messages

### Usage

```tsx
import { AnonymousChat } from "@/components/anonymous-chat"

export default function Page() {
  return (
    <div>
      {/* Your page content */}
      <AnonymousChat />
    </div>
  )
}
```

### WebSocket URL

Update in `anonymous-chat.tsx` if using different host:

```typescript
const wsUrl = `ws://localhost:8000/chat/ws/chat/${sessionId}`;
// For production:
// const wsUrl = `wss://your-domain.com/chat/ws/chat/${sessionId}`;
```

## Agent Behavior

### Automatic Transfer Scenarios

The agent will **suggest** human transfer when:

- Complex custom requests beyond standard packages
- Price negotiations
- Urgent issues or complaints
- Technical problems
- Questions outside its knowledge domain

### User-Initiated Transfer

Users can click **"Talk to a Human Agent"** button anytime.

### After Transfer

Once transferred:
- `is_handled_by_agent` = `false`
- `transferred_to_human` = `true`
- Agent **stops** responding to messages
- Messages wait for human admin response
- Transfer is **permanent** for that session

## Database Schema

### Session Model

```python
class Session(Base):
    __tablename__ = "sessions"

    session_id: str (PK)
    linked_user_id: UUID (FK to users, nullable)
    created_at: datetime
    chat_history: str (JSON, nullable)
    
    # Agent/Human handoff
    is_handled_by_agent: bool (default=True)
    transferred_to_human: bool (default=False)
    transfer_reason: str (nullable)
```

### ChatMessage Model

```python
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: UUID (PK)
    session_id: str (FK to sessions)
    sender_type: Enum (user, admin, bot)
    message: str
    timestamp: datetime
```

## Admin Dashboard (Future)

To handle transferred chats, you'll need an admin dashboard with:

1. **Active Chats List**: Show sessions where `transferred_to_human=True`
2. **Message Interface**: WebSocket connection to respond
3. **Session History**: View past messages
4. **Transfer Queue**: Prioritize urgent requests

## Testing the Agent

### 1. Test AI Responses

```bash
# Start backend
uvicorn app.main:app --reload

# Open frontend chat widget
# Ask: "What packages do you offer?"
# Ask: "Show me your themes"
# Ask: "What do customers say about you?"
```

### 2. Test Transfer

1. Click "Talk to a Human Agent"
2. Verify transfer message appears
3. Send new message
4. Verify "waiting for human" response

### 3. Test Knowledge Limits

Ask off-topic questions:
- "What's the weather today?"
- "Tell me a joke"
- "How do I bake a cake?"

Agent should redirect to business topics or suggest human transfer.

## Troubleshooting

### Agent Not Responding

**Check**:
1. `GOOGLE_API_KEY` set in `.env`
2. Database migration applied
3. Backend logs for errors
4. WebSocket connection established

### Wrong Information

**Cause**: Agent hallucinating or outdated data

**Fix**:
1. Update database with correct information
2. Tools query database in real-time
3. Adjust agent prompt in `lush_agent.py`

### Tool Errors

**Common Issue**: Database session not passed correctly

**Check**: `app/agents/lush_agent.py` - tools receive `db_session` parameter

### Connection Drops

**Frontend**: Implements auto-reconnect on WebSocket close

**Backend**: Gracefully handles disconnects, cleans up connections

## Customization

### Modify Agent Personality

Edit `SYSTEM_PROMPT` in `app/agents/lush_agent.py`:

```python
SYSTEM_PROMPT = """You are Lush Moments AI Assistant, a [YOUR DESCRIPTION]

[YOUR GUIDELINES]
"""
```

### Add New Tools

1. Create tool function in `lush_agent.py`:

```python
@tool
async def get_special_offers(db_session: AsyncSession) -> str:
    """Get current special offers and promotions"""
    # Your logic here
    return "Current offers..."
```

2. Add to tools list in `create_agent_graph()`:

```python
tools = [
    get_packages_info,
    get_themes_info,
    # ... existing tools
    get_special_offers,  # New tool
]
```

### Adjust AI Model

Change model in `get_llm()`:

```python
return ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # More powerful model
    temperature=0.5,  # Less creative (0.0-1.0)
    max_tokens=2048,  # Longer responses
)
```

## Performance Considerations

### Rate Limits

Google Gemini Free Tier:
- 15 requests per minute
- 1 million tokens per day

For production, consider:
- Caching common responses
- Rate limiting user messages
- Upgrading to paid tier

### Response Time

- Average: 1-3 seconds
- Database queries: <100ms
- AI generation: 1-2 seconds

### Scaling

For high traffic:
1. Use async everywhere (already implemented)
2. Connection pooling for WebSockets
3. Redis for session state
4. Load balancer for multiple backend instances

## Security

### Access Control

- **Agent**: Can read packages, themes, gallery, testimonials
- **Agent**: Cannot modify database
- **Agent**: Cannot access user personal information
- **Transfer**: Prevents agent from continuing after handoff

### Data Privacy

- Session IDs are randomly generated
- Messages stored in database
- No sensitive data exposed to AI
- User authentication separate from chat

## Next Steps

1. **Admin Dashboard**: Build interface for human agents
2. **Analytics**: Track common questions, transfer rates
3. **Improvements**: Fine-tune prompts based on user feedback
4. **Integrations**: Connect to booking system, CRM
5. **Multi-Language**: Support multiple languages

## Support

For questions or issues:
- Check backend logs: `tail -f app.log`
- Test WebSocket: Browser DevTools → Network → WS
- Verify database: `sqlite3 lush_moments.db`

## License

Part of Lush Moments Backend System
