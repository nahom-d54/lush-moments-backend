# Migration Guide - Admin Routes Reorganization

## Overview
This guide helps you migrate from the old route structure to the new organized admin structure.

## What Changed?

### Before (Old Structure)
```
/contact/messages                 → Admin endpoints mixed with public
/gallery/ (POST/PATCH/DELETE)     → Admin endpoints at root level
/contact-info/ (POST/PATCH/DELETE)→ Admin endpoints at root level
/bookings (GET all)               → Admin-only, but at public route
/bookings/{id} (PATCH)            → Admin endpoint at public route
```

### After (New Structure)
```
/admin/contact/messages           → All admin contact operations
/admin/gallery/                   → All admin gallery operations
/admin/contact-info/              → All admin contact info operations
/admin/bookings/                  → All admin booking operations
/bookings?email={email}           → Public: users can get their bookings
```

## URL Mapping

| Old Endpoint | New Endpoint | Notes |
|--------------|--------------|-------|
| `GET /contact/messages` | `GET /admin/contact/messages` | Admin only |
| `GET /contact/messages/{id}` | `GET /admin/contact/messages/{id}` | Admin only |
| `PATCH /contact/messages/{id}` | `PATCH /admin/contact/messages/{id}` | Admin only |
| `DELETE /contact/messages/{id}` | `DELETE /admin/contact/messages/{id}` | Admin only |
| `POST /gallery/` | `POST /admin/gallery/` | Admin only |
| `PATCH /gallery/{id}` | `PATCH /admin/gallery/{id}` | Admin only |
| `DELETE /gallery/{id}` | `DELETE /admin/gallery/{id}` | Admin only |
| `POST /contact-info/` | `POST /admin/contact-info/` | Admin only |
| `PATCH /contact-info/` | `PATCH /admin/contact-info/` | Admin only |
| `DELETE /contact-info/` | `DELETE /admin/contact-info/` | Admin only |
| `GET /bookings` (admin) | `GET /admin/bookings/` | Admin: view all bookings |
| `GET /bookings` (user) | `GET /bookings?email={email}` | Public: user's bookings |
| `PATCH /bookings/{id}` | `PATCH /admin/bookings/{id}` | Admin only |

## Code Migration Examples

### Frontend/API Client Updates

#### Contact Messages (Admin)
```javascript
// Before
const response = await fetch('/contact/messages', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// After
const response = await fetch('/admin/contact/messages', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

#### Gallery Management (Admin)
```javascript
// Before
await fetch('/gallery/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(galleryItem)
});

// After
await fetch('/admin/gallery/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(galleryItem)
});
```

#### User Bookings (Public)
```javascript
// Before (didn't exist - bookings were admin-only)
// Users couldn't retrieve their own bookings

// After (NEW FEATURE)
const response = await fetch(`/bookings?email=${userEmail}`);
const userBookings = await response.json();
```

#### Admin View All Bookings
```javascript
// Before
const response = await fetch('/bookings', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// After
const response = await fetch('/admin/bookings/', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## Database Migration
**No database changes required** - this is purely a routing reorganization.

## Testing Your Migration

### 1. Test Admin Endpoints
```bash
# Get admin token
TOKEN=$(curl -X POST http://localhost:8000/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}' \
  | jq -r '.access_token')

# Test new admin endpoints
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/admin/contact/messages
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/admin/gallery/
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/admin/bookings/
```

### 2. Test Public Endpoints
```bash
# These should work without authentication
curl http://localhost:8000/contact/
curl http://localhost:8000/gallery/
curl http://localhost:8000/contact-info/
curl "http://localhost:8000/bookings?email=test@example.com"
```

### 3. Verify Old Endpoints Return 404
```bash
# These should now return 404 Not Found
curl http://localhost:8000/contact/messages
curl -X POST http://localhost:8000/gallery/
```

## Rollback Plan

If you need to rollback to the old structure:

1. Restore the old route files from git:
   ```bash
   git checkout HEAD~1 -- app/routes/contact.py
   git checkout HEAD~1 -- app/routes/gallery.py
   git checkout HEAD~1 -- app/routes/contact_info.py
   git checkout HEAD~1 -- app/routes/bookings.py
   ```

2. Remove new admin files:
   ```bash
   rm app/routes/admin/contact.py
   rm app/routes/admin/gallery.py
   rm app/routes/admin/contact_info.py
   ```

3. Restore old main.py:
   ```bash
   git checkout HEAD~1 -- app/main.py
   ```

4. Restart the server

## Benefits of New Structure

✅ **Clear Separation**: Admin vs public routes clearly separated
✅ **Better Security**: Admin routes grouped and protected
✅ **Easier Maintenance**: Related endpoints in dedicated folders
✅ **Scalability**: Easy to add new admin endpoints
✅ **User Access**: Users can now retrieve their own bookings
✅ **RESTful Design**: Follows REST API best practices

## Support

If you encounter issues:
1. Check server logs for errors
2. Verify JWT token is valid
3. Ensure email parameter is provided for user bookings
4. Review ROUTES_STRUCTURE.md for complete endpoint list

---

**Migration Date**: October 2024
**Breaking Changes**: Yes (URL changes for admin endpoints)
**Database Changes**: None
**Recommended Testing**: Full regression test on admin panel
