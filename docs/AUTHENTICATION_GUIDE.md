# Authentication & OAuth Integration Guide

## Overview
The booking system now requires authentication. Users must create an account or login before creating bookings. Supports both traditional email/password and OAuth (Google, GitHub).

## Key Changes

### 🔒 Bookings Require Authentication
- **Before**: Anyone could create bookings with just an email
- **After**: Users must be logged in to create bookings
- **Security**: Users can only view their own bookings

### 👤 User Model Updates
- Added `auth_provider` field (local, google, github)
- Added `oauth_id` for OAuth provider user IDs
- Added `avatar_url` for profile pictures
- Added `last_login` timestamp
- Made `password_hash` nullable (OAuth users don't have passwords)

### 📝 Booking Model Updates
- Added `user_id` foreign key (required)
- User info fields now cached for reference
- Added relationship to User model

---

## Authentication Endpoints

### 1. Register (Email/Password)
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",  // optional
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "role": "client",
    "auth_provider": "local",
    "avatar_url": null
  }
}
```

### 2. Login (Email/Password)
```http
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** Same as register

### 3. OAuth Callback
```http
POST /auth/oauth/callback
Content-Type: application/json

{
  "provider": "google",  // or "github"
  "oauth_id": "123456789",
  "email": "john@example.com",
  "name": "John Doe",
  "avatar_url": "https://lh3.googleusercontent.com/..."
}
```

**Response:** Same as register

---

## OAuth Integration

### Frontend Implementation

The backend expects the frontend to:
1. Redirect user to OAuth provider (Google/GitHub)
2. Handle OAuth callback
3. Exchange code for user info
4. Send user info to backend `/auth/oauth/callback`

### Google OAuth Setup

1. **Create OAuth Client:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized redirect URI: `https://yourdomain.com/auth/google/callback`

2. **Frontend Implementation (React/Next.js example):**

```javascript
// Using @react-oauth/google
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';

function App() {
  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <GoogleLogin
        onSuccess={async (credentialResponse) => {
          // Decode JWT to get user info
          const decoded = jwtDecode(credentialResponse.credential);
          
          // Send to backend
          const response = await fetch('/auth/oauth/callback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              provider: 'google',
              oauth_id: decoded.sub,
              email: decoded.email,
              name: decoded.name,
              avatar_url: decoded.picture
            })
          });
          
          const data = await response.json();
          // Store token: localStorage.setItem('token', data.access_token)
        }}
        onError={() => console.log('Login Failed')}
      />
    </GoogleOAuthProvider>
  );
}
```

### GitHub OAuth Setup

1. **Create OAuth App:**
   - Go to GitHub Settings → Developer settings → OAuth Apps
   - Create new OAuth App
   - Add callback URL: `https://yourdomain.com/auth/github/callback`

2. **Frontend Implementation:**

```javascript
// Using OAuth redirect flow
function handleGitHubLogin() {
  const clientId = 'YOUR_GITHUB_CLIENT_ID';
  const redirectUri = 'https://yourdomain.com/auth/github/callback';
  const scope = 'read:user user:email';
  
  window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
}

// In callback page (/auth/github/callback)
async function handleGitHubCallback() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  
  // Exchange code for access token (server-side or via proxy)
  const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: 'YOUR_GITHUB_CLIENT_ID',
      client_secret: 'YOUR_GITHUB_CLIENT_SECRET',
      code: code
    })
  });
  const { access_token } = await tokenResponse.json();
  
  // Get user info
  const userResponse = await fetch('https://api.github.com/user', {
    headers: { 'Authorization': `Bearer ${access_token}` }
  });
  const githubUser = await userResponse.json();
  
  // Send to backend
  const response = await fetch('/auth/oauth/callback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: 'github',
      oauth_id: String(githubUser.id),
      email: githubUser.email,
      name: githubUser.name || githubUser.login,
      avatar_url: githubUser.avatar_url
    })
  });
  
  const data = await response.json();
  // Store token
}
```

---

## Updated Booking Endpoints

### Create Booking (Authenticated)
```http
POST /bookings
Authorization: Bearer {token}
Content-Type: application/json

{
  "event_type": "wedding",
  "event_date": "2024-06-15T14:00:00",
  "expected_guests": 150,
  "venue_location": "Grand Hotel Ballroom",
  "package_id": 1,
  "additional_details": "Outdoor ceremony",
  "special_requests": "Vegetarian options",
  // Optional - will use authenticated user's data if not provided:
  "full_name": "John Doe",
  "email": "john@example.com", 
  "phone": "+1234567890"
}
```

### Get My Bookings (Authenticated)
```http
GET /bookings
Authorization: Bearer {token}
```

**Response:** List of current user's bookings only

### Get Specific Booking (Authenticated)
```http
GET /bookings/{id}
Authorization: Bearer {token}
```

**Security:** Returns 403 if booking doesn't belong to authenticated user

---

## Frontend Flow

### 1. Check Authentication Status
```javascript
function isAuthenticated() {
  const token = localStorage.getItem('token');
  if (!token) return false;
  
  // Optionally verify token expiry
  try {
    const decoded = jwtDecode(token);
    return decoded.exp > Date.now() / 1000;
  } catch {
    return false;
  }
}
```

### 2. Protected Booking Flow
```javascript
async function handleBooking(bookingData) {
  if (!isAuthenticated()) {
    // Show login/register modal
    showAuthModal({
      message: 'Please login or create an account to book events',
      onSuccess: () => submitBooking(bookingData)
    });
    return;
  }
  
  await submitBooking(bookingData);
}

async function submitBooking(data) {
  const token = localStorage.getItem('token');
  
  const response = await fetch('/bookings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  
  if (response.status === 401) {
    // Token expired, redirect to login
    localStorage.removeItem('token');
    showAuthModal();
    return;
  }
  
  const result = await response.json();
  // Show success message
}
```

### 3. Handle 401 Globally
```javascript
// Axios interceptor example
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login?redirect=' + window.location.pathname;
    }
    return Promise.reject(error);
  }
);
```

---

## Database Migration

Run migrations to update database schema:

```bash
# Generate migration
alembic revision --autogenerate -m "Add OAuth support and booking user relationship"

# Apply migration
alembic upgrade head
```

**Or use CLI:**
```bash
python -m cli seed-db --clear  # Recreates tables
```

---

## Environment Variables

Add OAuth credentials to `.env`:

```env
# OAuth Configuration (Optional - for server-side OAuth)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
```

---

## Security Considerations

### ✅ Implemented
- JWT token authentication
- Password hashing with bcrypt
- User ownership verification for bookings
- OAuth provider validation
- Email uniqueness across providers

### 🔒 Best Practices
1. **HTTPS Only**: Always use HTTPS in production
2. **Token Storage**: Store tokens securely (httpOnly cookies preferred over localStorage)
3. **CORS**: Configure CORS properly for your frontend domain
4. **Rate Limiting**: Add rate limiting to auth endpoints
5. **OAuth Secrets**: Never expose OAuth secrets in frontend code

### 📋 Recommended Additions
```python
# Rate limiting example
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(...):
    ...
```

---

## Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"TestPass123!"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Create Booking (with token)
curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"wedding","event_date":"2024-12-25T14:00:00",...}'
```

### Test OAuth Flow
```bash
# Simulate OAuth callback
curl -X POST http://localhost:8000/auth/oauth/callback \
  -H "Content-Type: application/json" \
  -d '{
    "provider":"google",
    "oauth_id":"123456789",
    "email":"oauth@example.com",
    "name":"OAuth User",
    "avatar_url":"https://example.com/avatar.jpg"
  }'
```

---

## Error Handling

### Common Errors

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```
**Action:** Redirect to login

**403 Forbidden:**
```json
{
  "detail": "Not authorized to access this booking"
}
```
**Action:** User trying to access another user's booking

**400 Bad Request:**
```json
{
  "detail": "Email already registered with google provider"
}
```
**Action:** User trying to register with OAuth but email exists with different provider

---

## Migration from Old System

### For Existing Bookings
Old bookings without `user_id` need to be handled:

```python
# Option 1: Create placeholder users for existing bookings
# Option 2: Mark old bookings as legacy (add is_legacy flag)
# Option 3: Contact customers to create accounts and claim bookings
```

### Frontend Migration Checklist
- [ ] Add login/register UI
- [ ] Implement OAuth buttons (Google, GitHub)
- [ ] Add token storage and management
- [ ] Update booking form to check authentication
- [ ] Add "My Bookings" page for authenticated users
- [ ] Handle 401 errors globally
- [ ] Add auth state management (Redux/Context)
- [ ] Test OAuth flows in production

---

**Date**: October 2024
**Version**: 2.0
**Breaking Change**: ⚠️ Yes - Bookings now require authentication
