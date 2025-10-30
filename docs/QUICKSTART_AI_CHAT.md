# Quick Start: AI Chat Agent Setup

## Prerequisites

- Backend running (FastAPI)
- Database migrated
- Google Gemini API key

## Step-by-Step Setup

### 1. Get Google Gemini API Key

```bash
# Visit: https://aistudio.google.com/app/apikey
# Create API key
# Copy it
```

### 2. Configure Environment

Add to `.env` file:

```bash
GOOGLE_API_KEY=your-actual-api-key-here
```

### 3. Apply Database Migration

```bash
# From backend directory
alembic upgrade head
```

### 4. Start Backend

```bash
uvicorn app.main:app --reload
```

### 5. Test the Chat

**Option A: Use Frontend**
- Open your Next.js app
- Click the chat bubble (bottom right)
- Start chatting!

**Option B: Use WebSocket Test Tool**
```javascript
// Open browser console
const ws = new WebSocket('ws://localhost:8000/chat/ws/chat/test-session-123');

ws.onopen = () => {
  console.log('Connected!');
  ws.send(JSON.stringify({
    type: 'message',
    message: 'What packages do you offer?'
  }));
};

ws.onmessage = (event) => {
  console.log('Received:', JSON.parse(event.data));
};
```

## Test Questions

Try these to see the agent in action:

1. "What packages do you offer?"
2. "Show me your decoration themes"
3. "What do customers say about your service?"
4. "How do I book an event?"
5. "Tell me about your payment options"

## Transfer to Human

Click the **"Talk to a Human Agent"** button in the chat to test transfer functionality.

## Common Issues

### Agent not responding
- Check `GOOGLE_API_KEY` is set in `.env`
- Check backend logs for errors
- Verify database migration applied

### Connection failed
- Ensure backend is running on port 8000
- Check WebSocket URL in frontend (`ws://localhost:8000`)

### Database errors
- Run: `alembic upgrade head`
- Check `lush_moments.db` exists

## File Structure

```
app/
├── agents/
│   └── lush_agent.py          # AI agent logic
├── routes/
│   └── chat.py                # WebSocket & endpoints
├── models/
│   ├── session.py             # Session model (updated)
│   └── chat_message.py        # Message model

frontend/
└── components/
    └── anonymous-chat.tsx     # Chat widget (updated)
```

## What's New

✅ **AI-Powered Responses**: Gemini 1.5 Flash model
✅ **Database Tools**: Real-time access to packages, themes, etc.
✅ **Agent → Human Transfer**: Seamless handoff
✅ **WebSocket Integration**: Real-time bidirectional chat
✅ **Session Persistence**: Tracks agent vs human handling

## Next Steps

- Read full documentation: `AI_AGENT_DOCUMENTATION.md`
- Build admin dashboard for human agents
- Customize agent personality in `lush_agent.py`
- Add more database tools as needed

## Need Help?

Check logs:
```bash
# Backend logs will show agent processing
tail -f app.log
```

Test WebSocket:
```bash
# Browser DevTools → Network → WS filter
```

Verify database:
```bash
sqlite3 lush_moments.db
SELECT * FROM sessions LIMIT 5;
```
