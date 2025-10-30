# Chat Session Merging Implementation

## Overview
This document explains how anonymous chat sessions are automatically merged with user accounts when they login or register.

## How It Works

### 1. **Anonymous Chat Session**
When a user visits the site and starts chatting without being logged in:
- A unique `session_id` is generated in the frontend (e.g., `session-1730234567890-abc123`)
- This `session_id` is stored in `localStorage` with key `lush-moments-chat-session`
- All chat messages are associated with this `session_id` in the backend database
- The session exists in the `sessions` table with `linked_user_id = NULL`

### 2. **User Decides to Login/Register**
When visiting `/booking`, users are redirected to `/auth` if not authenticated with a toast message:
- **Toast Message**: "Please login or create an account before booking an event."
- Redirect URL includes the return path (e.g., `/auth?mode=login&redirect=/booking`)

### 3. **Session Merging on Auth**
When the user logs in or registers:

**Frontend (`lib/auth.ts`)**:
```typescript
// Automatically retrieves session_id from localStorage
const sessionId = localStorage.getItem("lush-moments-chat-session");

// Sends it with login/register request
authApi.login({ email, password, session_id: sessionId });
authApi.register({ name, email, password, session_id: sessionId });
```

**Backend (`app/routes/auth.py`)**:
```python
# Helper function merges the session
await merge_anonymous_session(db, user.id, session_id)
```

The `merge_anonymous_session` function:
1. Finds the session by `session_id`
2. Checks if it's not already linked to another user
3. Links the session to the newly authenticated user by setting `linked_user_id = user.id`
4. All chat history is now associated with the user's account

### 4. **Chat History Preservation**
- **New Account**: Anonymous chat → Creates session → User registers → Session linked to new account
- **Existing Account**: Anonymous chat → Creates session → User logs in → Session linked to existing account
- All messages remain in the `chat_messages` table linked to the `session_id`
- Users can access their chat history via `/chat/my-sessions` endpoint

## Database Schema

### Sessions Table
```python
class Session(Base):
    session_id: str (PK)           # e.g., "session-1730234567890-abc123"
    linked_user_id: UUID | None    # NULL for anonymous, user_id when merged
    created_at: datetime
    
    # Relationships
    user: User
    messages: List[ChatMessage]
```

### Chat Messages Table
```python
class ChatMessage(Base):
    id: UUID (PK)
    session_id: str (FK → sessions)
    sender_type: Enum["user", "admin", "bot"]
    message: str
    timestamp: datetime
    
    # Relationships
    session: Session
```

## API Endpoints

### Authentication (Auto-merges sessions)
```
POST /auth/register
POST /auth/login
POST /auth/oauth/callback

Request Body:
{
  "email": "user@example.com",
  "password": "password123",
  "session_id": "session-1730234567890-abc123"  // Optional, auto-sent by frontend
}
```

### Chat Management
```
GET /chat/history/{session_id}
  - Get all messages for a session
  
GET /chat/my-sessions
  - Get all sessions linked to authenticated user
  - Requires authentication
  - Returns session list with message counts and last message

POST /chat/merge-session
  - Manually merge a session (alternative to auto-merge)
  - Requires authentication
  Body: { "anonymous_session_id": "session-..." }
```

### WebSocket Chat
```
WS /ws/chat/{session_id}
  - Real-time chat with admin/bot
  - Creates session if doesn't exist
  - Messages automatically saved to database
```

## Frontend Implementation

### Booking Page Protection
```tsx
// In app/booking/page.tsx
useEffect(() => {
  if (!authLoading && !user) {
    toast({
      title: "Authentication Required",
      description: "Please login or create an account before booking an event.",
      variant: "destructive",
    });
    
    router.push(`/auth?mode=login&redirect=/booking`);
  }
}, [user, authLoading, router, toast]);
```

### Anonymous Chat Component
```tsx
// Generates and stores session_id in localStorage
useEffect(() => {
  let storedSessionId = localStorage.getItem("lush-moments-chat-session");
  if (!storedSessionId) {
    storedSessionId = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem("lush-moments-chat-session", storedSessionId);
  }
  setSessionId(storedSessionId);
}, []);
```

## User Flow Examples

### Example 1: New User with Chat History
1. User visits site (not logged in)
2. Opens anonymous chat widget
3. Session created: `session-1730234567890-abc123`
4. User chats with bot/admin (5 messages saved)
5. User clicks "Book Event"
6. Redirected to `/auth?mode=login&redirect=/booking` with toast
7. User creates new account
8. **Backend automatically links session to new user**
9. User can now see their 5 previous messages in chat history
10. Redirected back to `/booking`

### Example 2: Returning User with New Session
1. Logged out user visits site
2. Opens chat, new session created: `session-1730234567891-xyz789`
3. Chats with support (3 messages)
4. User tries to book event
5. Redirected to login with toast
6. User logs in with existing credentials
7. **Backend links new session to existing account**
8. User now has 2 sessions in their account:
   - Old session (from previous visit)
   - New session (from today)

### Example 3: Session Hijacking Prevention
1. User A creates anonymous session: `session-123`
2. User A logs in → Session linked to User A
3. User B somehow gets session ID `session-123`
4. User B tries to login
5. **Backend detects session already linked to User A**
6. **Does NOT merge** - prevents session hijacking
7. User B gets their own new session

## Security Considerations

### ✅ Implemented Protections
1. **One-time merging**: Sessions can only be linked to one user
2. **No re-linking**: Once linked, sessions cannot be moved to another user
3. **Silent failure**: Failed merges don't break auth flow
4. **Validation**: Session existence checked before linking
5. **User ownership**: Only session owner can access messages via API

### ⚠️ Recommendations for Production
1. Add session expiration (e.g., 30 days inactive)
2. Implement rate limiting on chat endpoints
3. Add message encryption for sensitive content
4. Admin authentication for accessing user sessions
5. Audit logging for session merges
6. Consider IP verification for session creation

## Testing

### Test Cases

**Test 1: Basic Session Merge**
```bash
# Create anonymous session
curl -X POST http://localhost:8000/ws/chat/test-session-123

# Send messages
# (via WebSocket)

# Register with session_id
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "session_id": "test-session-123"
  }'

# Verify session linked
curl http://localhost:8000/chat/history/test-session-123
```

**Test 2: Login with Existing Session**
```bash
# Login with session_id
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "session_id": "test-session-456"
  }'

# Check user's sessions
curl http://localhost:8000/chat/my-sessions \
  -H "Authorization: Bearer <token>"
```

## Troubleshooting

### Issue: Session Not Merging
**Symptom**: Chat history not visible after login

**Solutions**:
1. Check browser localStorage for `lush-moments-chat-session` key
2. Verify session exists in database
3. Check backend logs for merge errors
4. Ensure `session_id` is being sent in auth request

### Issue: Duplicate Sessions
**Symptom**: Multiple sessions for same user

**Explanation**: This is normal! Each browser/device creates its own session.
Users can have multiple sessions (desktop, mobile, etc.)

**Solution**: Display all sessions in user's chat history

### Issue: Lost Messages
**Symptom**: Messages disappear after login

**Solutions**:
1. Check if session was properly created before login
2. Verify `session_id` matches between localStorage and database
3. Check for session ID changes (localStorage cleared?)

## Future Enhancements

### Planned Features
- [ ] Admin dashboard to view all active sessions
- [ ] Real-time admin response notifications
- [ ] File/image upload in chat
- [ ] Chat session export (download history)
- [ ] Multi-device sync for logged-in users
- [ ] Push notifications for new messages
- [ ] AI-powered auto-responses
- [ ] Chat analytics (response time, satisfaction)

### Performance Optimizations
- [ ] Cache session data in Redis
- [ ] Pagination for chat history
- [ ] WebSocket connection pooling
- [ ] Message batching for high-traffic periods

---

## Quick Reference

**Frontend Session ID Storage**:
- Key: `lush-moments-chat-session`
- Format: `session-${timestamp}-${random}`

**Backend Merge Function**:
- Location: `app/routes/auth.py`
- Function: `merge_anonymous_session()`

**Chat Routes**:
- WebSocket: `/ws/chat/{session_id}`
- History: `/chat/history/{session_id}`
- User Sessions: `/chat/my-sessions`
- Manual Merge: `/chat/merge-session`

**Booking Protection**:
- File: `app/booking/page.tsx`
- Redirects to: `/auth?mode=login&redirect=/booking`
- Toast: "Authentication Required - Please login before booking"
