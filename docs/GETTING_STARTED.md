# 🚀 Getting Started with the Enhanced Backend

## Quick Migration Guide

### Step 1: Install New Dependencies
```bash
uv sync
```

### Step 2: Reset Database with New Structure
```bash
# IMPORTANT: This will delete all existing data
# Back up your database first if you have important data!

# Option A: Using CLI (Recommended)
uv run python cli.py seed-db --clear

# Option B: Using Python directly
uv run python -m app.seeders.seed
```

### Step 3: Start the Server
```bash
uv run uvicorn app.main:app --reload
```

### Step 4: Visit API Documentation
Open your browser: **http://127.0.0.1:8000/docs**

---

## 🎯 What's New?

### 1. Contact Form (`/contact/`)
- Accepts: full_name, email, phone_number, message
- Sends automatic emails to user and admin
- Admin can view/manage submissions at `/contact/messages`

### 2. Gallery System (`/gallery/`)
- Upload images with title, description, category, tags
- Filter by category or featured items
- Supports thumbnails for fast loading

### 3. Contact Info (`/contact-info/`)
- Single endpoint for all business contact information
- Email, phone, location, business hours, social media links
- Admin can update via PATCH request

### 4. Enhanced Packages
- **Now with bullet points!** No more comma-separated strings
- Each package has multiple `PackageItem` records
- Supports `is_popular` flag and `display_order`
- Field renamed: `name` → `title`

### 5. Enhanced Bookings
- Detailed user info: full_name, email, phone (no more JSON)
- Event details: event_type (dropdown), event_date, expected_guests
- Venue location, package selection
- Additional details and special requests fields
- Admin notes for internal use
- Status tracking with timestamps

---

## 📋 Testing the New Features

### Test Contact Form
```bash
curl -X POST "http://127.0.0.1:8000/contact/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone_number": "+1-555-0000",
    "message": "This is a test message"
  }'
```

**Expected Response:**
```json
{
  "message": "Thank you for contacting us! We'll get back to you soon.",
  "id": 3
}
```

### Test Gallery
```bash
# Get all gallery items
curl "http://127.0.0.1:8000/gallery/"

# Filter by category
curl "http://127.0.0.1:8000/gallery/?category=wedding"

# Get only featured items
curl "http://127.0.0.1:8000/gallery/?featured_only=true"
```

### Test Contact Info
```bash
curl "http://127.0.0.1:8000/contact-info/"
```

**Expected Response:**
```json
{
  "id": 1,
  "email": "info@lushmoments.com",
  "phone": "+1-555-LUSH-MOMENTS",
  "location": "123 Event Plaza, Suite 456, Los Angeles, CA 90001",
  "business_hours": "{\"monday\":\"9:00 AM - 6:00 PM\",...}",
  "facebook_url": "https://facebook.com/lushmoments",
  ...
}
```

### Test Enhanced Packages
```bash
curl "http://127.0.0.1:8000/packages"
```

**New Response Format:**
```json
[
  {
    "id": 1,
    "title": "Starter Package",
    "description": "Perfect for small intimate gatherings",
    "price": 500.0,
    "is_popular": false,
    "display_order": 1,
    "items": [
      {
        "id": 1,
        "package_id": 1,
        "item_text": "Venue accommodation for up to 50 guests",
        "display_order": 0
      },
      {
        "id": 2,
        "package_id": 1,
        "item_text": "Basic catering services with 3 meal options",
        "display_order": 1
      }
      ...
    ]
  }
]
```

### Test Enhanced Bookings
```bash
curl -X POST "http://127.0.0.1:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith",
    "email": "john@example.com",
    "phone": "+1-555-1234",
    "event_type": "Wedding",
    "event_date": "2025-06-15T14:00:00",
    "expected_guests": 150,
    "venue_location": "Grand Ballroom",
    "package_id": 2,
    "additional_details": "Outdoor ceremony",
    "special_requests": "Vegetarian menu"
  }'
```

**Expected Response:**
```json
{
  "message": "Your booking request has been submitted successfully! You'll receive a confirmation email shortly.",
  "booking_id": 4,
  "confirmation_email_sent": true
}
```

---

## 🗄️ Database Changes

### New Tables
1. `contact_messages` - Contact form submissions
2. `gallery_items` - Gallery images with metadata
3. `contact_info` - Business contact information
4. `package_items` - Bullet points for packages

### Modified Tables
1. `packages`:
   - Removed: `name`, `included_items`
   - Added: `title`, `is_popular`, `display_order`
   - Added relationship to `package_items`

2. `event_bookings`:
   - Removed: `client_info` (JSON), `date`, `venue`, `message`
   - Added: `full_name`, `email`, `phone`, `event_date`, `expected_guests`, `venue_location`, `additional_details`, `special_requests`, `admin_notes`, `created_at`, `updated_at`
   - Added: `cancelled` status option

---

## 📧 Email Configuration (Optional)

Emails will log to console if SMTP is not configured. To enable real emails:

### For Gmail:
1. Enable 2FA on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@lushmoments.com
SMTP_USE_TLS=True
ADMIN_EMAIL=admin@lushmoments.com
BUSINESS_PHONE=+1-555-123-4567
```

### Email Templates Included:
- ✅ Contact form confirmation (to user)
- ✅ Contact form notification (to admin)
- ✅ Booking confirmation (to customer)
- ✅ Booking notification (to admin)

---

## 🎨 Frontend Integration Examples

### Display Package Items as Bullets
```javascript
// Fetch package
const response = await fetch('/packages/1');
const package = await response.json();

// Render items
package.items.forEach(item => {
  console.log(`• ${item.item_text}`);
});
```

### Gallery with Category Filter
```javascript
// Get categories
const catResponse = await fetch('/gallery/categories');
const { categories } = await catResponse.json();

// Filter by category
const galleryResponse = await fetch(`/gallery/?category=${selectedCategory}`);
const { items } = await galleryResponse.json();
```

### Business Hours Display
```javascript
// Fetch contact info
const response = await fetch('/contact-info/');
const info = await response.json();

// Parse hours
const hours = JSON.parse(info.business_hours);
Object.entries(hours).forEach(([day, time]) => {
  console.log(`${day}: ${time}`);
});
```

---

## 🔐 Admin Endpoints (Require Authentication)

### Login First
```bash
# Login as admin
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@lushmoments.com",
    "password": "Admin@123"
  }'

# Save the access_token from response
```

### View Contact Messages
```bash
curl "http://127.0.0.1:8000/contact/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# View unread only
curl "http://127.0.0.1:8000/contact/messages?unread_only=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Manage Gallery
```bash
# Create gallery item
curl -X POST "http://127.0.0.1:8000/gallery/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Wedding",
    "description": "A stunning outdoor wedding",
    "image_url": "/uploads/wedding1.jpg",
    "category": "wedding",
    "tags": "[\"outdoor\", \"elegant\"]",
    "is_featured": true
  }'
```

### Update Booking Status
```bash
curl -X PATCH "http://127.0.0.1:8000/bookings/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "admin_notes": "Deposit received. Confirmed via phone."
  }'
```

---

## 📊 Sample Data Included

After running `seed-db --clear`, you'll have:

- ✅ 2 users (admin + client)
- ✅ 4 packages with bullet points (40+ total items)
- ✅ 5 gallery items (various categories)
- ✅ 1 contact info record
- ✅ 2 contact messages
- ✅ 6 themes
- ✅ 5 testimonials  
- ✅ 3 sample bookings
- ✅ 6 translations

---

## 🛠️ Troubleshooting

### "Table doesn't exist" Error
```bash
# Recreate all tables
uv run python cli.py init-db
uv run python cli.py seed-db
```

### Email Not Sending
- Check if SMTP settings are in `.env`
- If not configured, emails will log to console (this is expected)
- For Gmail, use App Password, not regular password

### Import Errors
```bash
# Reinstall dependencies
uv sync
```

### Can't Access Admin Endpoints
```bash
# Check if logged in
# Default admin credentials after seeding:
# Email: admin@lushmoments.com
# Password: Admin@123
```

---

## 📚 Documentation Files

- `PROFESSIONAL_ENHANCEMENT.md` - Complete technical documentation
- `QUICKSTART.md` - Original quick start guide
- `CLI.md` - CLI commands reference
- `README.md` - Project overview

---

## ✅ Next Steps

1. ✅ Reset database: `uv run python cli.py seed-db --clear`
2. ✅ Start server: `uv run uvicorn app.main:app --reload`
3. ✅ Test endpoints at http://127.0.0.1:8000/docs
4. ✅ Configure SMTP for emails (optional)
5. ✅ Build frontend to consume the API

---

## 🎉 You're Ready!

Your backend now has:
- ✅ Professional contact form with email notifications
- ✅ Complete gallery management system
- ✅ Centralized business contact information
- ✅ Enhanced packages with bullet points
- ✅ Detailed booking system with proper fields
- ✅ All the features of a professional event management platform!

For questions, check the API docs at `/docs` or review `PROFESSIONAL_ENHANCEMENT.md`.

**Happy coding! 🚀**
