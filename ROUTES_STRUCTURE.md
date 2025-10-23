# Routes Structure - Reorganized

## Overview
All admin endpoints have been moved to the `/admin` folder for better organization and security.

## Public Routes (No Authentication)

### `/contact` - Contact Form Submission
- **POST** `/contact/` - Submit contact form
  - File: `app/routes/contact.py`

### `/gallery` - Gallery Browsing
- **GET** `/gallery/` - Browse gallery items
- **GET** `/gallery/categories` - Get categories
- **GET** `/gallery/{id}` - Get specific item
  - File: `app/routes/gallery.py`

### `/contact-info` - Business Information
- **GET** `/contact-info/` - Get business contact details
  - File: `app/routes/contact_info.py`

### `/bookings` - Event Bookings
- **POST** `/bookings` - Create new booking
- **GET** `/bookings?email={email}` - Get user's bookings by email
- **GET** `/bookings/{id}` - Get specific booking
  - File: `app/routes/bookings.py`

---

## Admin Routes (Require JWT Authentication)

### `/admin/contact` - Contact Message Management
- **GET** `/admin/contact/messages` - List all messages
- **GET** `/admin/contact/messages/{id}` - Get specific message
- **PATCH** `/admin/contact/messages/{id}` - Mark as read
- **DELETE** `/admin/contact/messages/{id}` - Delete message
  - File: `app/routes/admin/contact.py`

### `/admin/gallery` - Gallery Management
- **POST** `/admin/gallery/` - Create gallery item
- **PATCH** `/admin/gallery/{id}` - Update gallery item
- **DELETE** `/admin/gallery/{id}` - Delete gallery item
  - File: `app/routes/admin/gallery.py`

### `/admin/contact-info` - Business Info Management
- **POST** `/admin/contact-info/` - Create contact info
- **PATCH** `/admin/contact-info/` - Update contact info
- **DELETE** `/admin/contact-info/` - Delete contact info
  - File: `app/routes/admin/contact_info.py`

### `/admin/bookings` - Booking Management
- **GET** `/admin/bookings/` - List all bookings (with filters)
- **GET** `/admin/bookings/{id}` - Get specific booking
- **PATCH** `/admin/bookings/{id}` - Update status/notes
- **DELETE** `/admin/bookings/{id}` - Delete booking
  - File: `app/routes/admin/bookings.py`

### `/admin/packages` - Package Management
- **GET** `/admin/packages/` - List all packages
- **POST** `/admin/packages/` - Create package
- **PATCH** `/admin/packages/{id}` - Update package
- **DELETE** `/admin/packages/{id}` - Delete package
  - File: `app/routes/admin/packages.py`

### Other Admin Routes
- `/admin/themes` - Theme management
- `/admin/testimonials` - Testimonial management
- `/admin/sessions` - Session management
- `/admin/translations` - Translation management

---

## Key Changes

### 1. Admin Endpoints Moved to `/admin` Prefix
All administrative operations now use the `/admin/*` prefix, making it clear which endpoints require authentication.

### 2. User Booking Retrieval
- **Before**: `GET /bookings` was admin-only (view all bookings)
- **After**: `GET /bookings?email={email}` is public (users can view their own bookings by providing email)
- **Admin**: `GET /admin/bookings/` lists all bookings

### 3. File Organization
```
app/routes/
├── admin/                    # All admin endpoints
│   ├── contact.py           # NEW: Contact message management
│   ├── gallery.py           # NEW: Gallery management
│   ├── contact_info.py      # NEW: Contact info management
│   ├── bookings.py          # UPDATED: All booking admin ops
│   ├── packages.py          # Existing
│   ├── themes.py            # Existing
│   ├── testimonials.py      # Existing
│   ├── sessions.py          # Existing
│   └── translations.py      # Existing
├── contact.py               # UPDATED: Only public submission
├── gallery.py               # UPDATED: Only public browsing
├── contact_info.py          # UPDATED: Only public viewing
├── bookings.py              # UPDATED: Public booking ops
└── ... (other public routes)
```

---

## Migration Notes

### Breaking Changes
1. **Contact Messages**: Moved from `/contact/messages` to `/admin/contact/messages`
2. **Gallery Admin**: Moved from `/gallery/` POST/PATCH/DELETE to `/admin/gallery/`
3. **Contact Info Admin**: Moved from `/contact-info/` POST/PATCH/DELETE to `/admin/contact-info/`
4. **Booking Admin List**: Moved from `/bookings` (admin-only) to `/admin/bookings/`
5. **Booking Admin Update**: Moved from `/bookings/{id}` PATCH to `/admin/bookings/{id}` PATCH

### Non-Breaking Changes
- Public endpoints remain unchanged
- Authentication mechanism unchanged
- Response formats unchanged

---

## Testing the New Structure

### Test Public Access
```bash
# Should work without authentication
curl http://localhost:8000/contact/
curl http://localhost:8000/gallery/
curl http://localhost:8000/bookings?email=test@example.com
```

### Test Admin Access
```bash
# Get token
TOKEN=$(curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}' \
  | jq -r '.access_token')

# Use token
curl http://localhost:8000/admin/contact/messages \
  -H "Authorization: Bearer $TOKEN"
```

---

**Date**: October 2024
**Version**: 2.0
**Status**: ✅ All routes reorganized and secured
