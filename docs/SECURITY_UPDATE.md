# Security Update - Admin Endpoint Protection

## Overview
All admin endpoints have been secured with JWT authentication and organized into the `/admin` folder structure. This ensures proper separation of public and administrative operations.

## New Structure

### Admin Routes Organization
All admin endpoints are now under `/admin/*` prefix:
- `/admin/contact/*` - Contact message management
- `/admin/gallery/*` - Gallery item management
- `/admin/contact-info/*` - Business contact information management
- `/admin/bookings/*` - Booking management (view all, update status)
- `/admin/packages/*` - Package management
- `/admin/themes/*` - Theme management
- `/admin/testimonials/*` - Testimonial management
- `/admin/sessions/*` - Session management
- `/admin/translations/*` - Translation management

### Public Routes
Public endpoints remain at the root level:
- `/contact` - Submit contact form
- `/gallery` - Browse gallery items
- `/contact-info` - View business information
- `/bookings` - Create and view user's own bookings
- `/packages` - View available packages
- (and other public routes)

## Changes Made

### 1. Contact Messages (`app/routes/admin/contact.py`)
**Admin Endpoints:**
- `GET /admin/contact/messages` - List all contact form submissions
- `GET /admin/contact/messages/{id}` - Get specific contact message
- `PATCH /admin/contact/messages/{id}` - Mark message as read/responded
- `DELETE /admin/contact/messages/{id}` - Delete contact message

**Public Endpoints** (`app/routes/contact.py`):
- `POST /contact/` - Submit contact form (no auth required)

---

### 2. Gallery Management (`app/routes/admin/gallery.py`)
**Admin Endpoints:**
- `POST /admin/gallery/` - Create new gallery item
- `PATCH /admin/gallery/{id}` - Update gallery item
- `DELETE /admin/gallery/{id}` - Delete gallery item

**Public Endpoints** (`app/routes/gallery.py`):
- `GET /gallery/` - Browse gallery (with filters)
- `GET /gallery/categories` - Get available categories
- `GET /gallery/{id}` - View single gallery item

---

### 3. Contact Information (`app/routes/admin/contact_info.py`)
**Admin Endpoints:**
- `POST /admin/contact-info/` - Create business contact info
- `PATCH /admin/contact-info/` - Update business contact info
- `DELETE /admin/contact-info/` - Delete contact info

**Public Endpoints** (`app/routes/contact_info.py`):
- `GET /contact-info/` - View business contact information

---

### 4. Booking Management

**Admin Endpoints** (`app/routes/admin/bookings.py`):
- `GET /admin/bookings/` - List all bookings (with filters)
- `GET /admin/bookings/{id}` - View specific booking
- `PATCH /admin/bookings/{id}` - Update booking status/admin notes
- `DELETE /admin/bookings/{id}` - Delete booking

**Public Endpoints** (`app/routes/bookings.py`):
- `POST /bookings` - Create new booking
- `GET /bookings?email={email}` - Get user's bookings by email (requires email parameter)
- `GET /bookings/{id}` - View specific booking

**Important Change**: `GET /bookings` now requires an `email` query parameter to fetch bookings for a specific user, making it accessible to customers without admin authentication.

---

## Testing Authentication

### 1. Get Admin JWT Token
```bash
POST /admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 2. Use Token in Admin Requests
```bash
GET /admin/contact/messages
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 3. Public Endpoints (No Token Required)
```bash
# Submit contact form
POST /contact/

# View gallery
GET /gallery/

# Get business contact info
GET /contact-info/

# Create booking
POST /bookings

# Get user's bookings
GET /bookings?email=user@example.com
```

### 4. Expected Responses

**Without Token on Admin Endpoint (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

**With Invalid Token (403 Forbidden):**
```json
{
  "detail": "Could not validate credentials"
}
```

**With Valid Token (200 OK):**
```json
{
  "data": [...]
}
```

---

## Security Best Practices

### ✅ Implemented
- JWT token authentication on all admin endpoints
- Password hashing for admin accounts
- Separation of public and admin routes
- Token expiration (configurable in settings)

### 🔐 Recommended for Production
1. **HTTPS Only**: Ensure all requests use HTTPS in production
2. **Token Refresh**: Implement refresh tokens for longer sessions
3. **Rate Limiting**: Add rate limiting to prevent brute force attacks
4. **Audit Logging**: Log all admin actions for security monitoring
5. **Password Policy**: Enforce strong password requirements
6. **CORS Configuration**: Restrict CORS origins in production
7. **Environment Variables**: Never commit `.env` file to version control

### Example Rate Limiting (Future Enhancement)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/admin/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def admin_login(...):
    ...
```

---

## Testing Checklist

**Admin Endpoints (Require Authentication):**
- [ ] Test `/admin/contact/messages` without token (should return 401)
- [ ] Test `/admin/contact/messages` with valid token (should succeed)
- [ ] Test `/admin/gallery/` POST without token (should return 401)
- [ ] Test `/admin/gallery/` POST with valid token (should succeed)
- [ ] Test `/admin/contact-info/` PATCH without token (should return 401)
- [ ] Test `/admin/contact-info/` PATCH with valid token (should succeed)
- [ ] Test `/admin/bookings/` without token (should return 401)
- [ ] Test `/admin/bookings/` with valid token (should succeed)

**Public Endpoints (No Authentication Required):**
- [ ] Test contact form submission (`POST /contact/`)
- [ ] Test gallery browsing (`GET /gallery/`)
- [ ] Test booking creation (`POST /bookings`)
- [ ] Test user bookings retrieval (`GET /bookings?email=test@example.com`)
- [ ] Verify business info accessible (`GET /contact-info/`)

**Token Behavior:**
- [ ] Test token expiration behavior
- [ ] Test invalid token handling
- [ ] Verify admin login works correctly

---

## Rollback Instructions

If you need to temporarily disable authentication for testing:

1. Comment out the `current_admin=Depends(get_current_admin)` parameters
2. Restart the server
3. **IMPORTANT:** Re-enable before deploying to production!

---

## Additional Resources

- JWT Documentation: https://jwt.io/
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- OAuth2 with Password Flow: https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/

---

**Date Updated:** 2024
**Version:** 1.0
**Status:** ✅ All Admin Endpoints Secured
