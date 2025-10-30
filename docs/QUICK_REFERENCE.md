# ⚡ Quick Reference - Essential Commands & Endpoints

## 🚀 Quick Start (3 Steps)

```bash
# 1. Install dependencies
uv sync

# 2. Reset database with new structure
uv run python cli.py seed-db --clear

# 3. Start server
uv run uvicorn app.main:app --reload
```

**Server:** http://127.0.0.1:8000  
**API Docs:** http://127.0.0.1:8000/docs  
**Admin Login:** admin@lushmoments.com / Admin@123

---

## 📋 Key Endpoints

### Public Endpoints (No Auth)
```
GET    /packages              - All packages with bullet points
POST   /contact/              - Submit contact form
GET    /gallery/              - Browse gallery
GET    /contact-info/         - Business contact info
POST   /bookings              - Create event booking
```

### Admin Endpoints (Auth Required)
```
POST   /auth/login            - Login (get token)
GET    /contact/messages      - View contact submissions
GET    /admin/packages/       - Manage packages
PATCH  /bookings/{id}         - Update booking status
POST   /gallery/              - Upload gallery item
```

---

## 🔐 Admin Access

```bash
# Login
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@lushmoments.com","password":"Admin@123"}'

# Use token in requests
curl "http://127.0.0.1:8000/contact/messages" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 New Data Models

### Package Structure (No More Comma-Separated!)
```json
{
  "title": "Classic Package",
  "price": 1200.0,
  "items": [
    {"item_text": "Venue for 100 guests"},
    {"item_text": "Full catering"}
  ]
}
```

### Contact Form
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+1-555-1234",
  "message": "Your message here"
}
```

### Booking (Proper Fields!)
```json
{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1-555-5678",
  "event_type": "Wedding",
  "event_date": "2025-06-15T14:00:00",
  "expected_guests": 150,
  "venue_location": "Grand Ballroom",
  "package_id": 2,
  "additional_details": "...",
  "special_requests": "..."
}
```

---

## 🎯 What Changed

| Feature | Old | New |
|---------|-----|-----|
| Package items | Comma-separated string | Bullet point list (PackageItem table) |
| Package name | `name` | `title` |
| Booking user info | JSON string | Direct fields (full_name, email, phone) |
| Booking date | `date` | `event_date` |
| Booking venue | `venue` | `venue_location` |
| Contact form | ❌ None | ✅ Full system with emails |
| Gallery | ❌ None | ✅ Full system with categories |
| Contact info | ❌ None | ✅ Centralized endpoint |

---

## 📧 Email Features

**Automatic Emails Sent:**
- ✅ Contact form → Confirmation to user + Notification to admin
- ✅ Booking → Confirmation to customer + Notification to admin

**Configure in .env (optional):**
```env
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@lushmoments.com
```

**Note:** If not configured, emails log to console!

---

## 🛠️ CLI Commands

```bash
# Database
uv run python cli.py init-db          # Create tables
uv run python cli.py seed-db          # Seed data
uv run python cli.py seed-db --clear  # Clear & reseed

# Users
uv run python cli.py create-admin     # Create admin (interactive)
uv run python cli.py list-users       # List all users
uv run python cli.py list-admins      # List admin users

# Info
uv run python cli.py version          # Show version
```

---

## 🧪 Quick Test Commands

### Test Contact Form
```bash
curl -X POST "http://127.0.0.1:8000/contact/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name":"Test User",
    "email":"test@example.com",
    "phone_number":"+1-555-0000",
    "message":"Test message"
  }'
```

### Test Gallery
```bash
# All items
curl "http://127.0.0.1:8000/gallery/"

# By category
curl "http://127.0.0.1:8000/gallery/?category=wedding"

# Featured only
curl "http://127.0.0.1:8000/gallery/?featured_only=true"
```

### Test Packages (with bullet points)
```bash
curl "http://127.0.0.1:8000/packages"
```

### Test Booking
```bash
curl -X POST "http://127.0.0.1:8000/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name":"John Smith",
    "email":"john@example.com",
    "phone":"+1-555-1234",
    "event_type":"Wedding",
    "event_date":"2025-06-15T14:00:00",
    "expected_guests":150,
    "venue_location":"Grand Ballroom",
    "package_id":2
  }'
```

---

## 📦 Seeded Data

After `seed-db --clear`, you get:

| Entity | Count | Details |
|--------|-------|---------|
| Users | 2 | admin + client |
| Packages | 4 | With 40+ bullet point items |
| Gallery Items | 5 | Various categories |
| Contact Messages | 2 | Sample submissions |
| Bookings | 3 | Sample event bookings |
| Themes | 6 | Event themes |
| Testimonials | 5 | Customer reviews |
| Contact Info | 1 | Business information |

---

## 🎨 Frontend Tips

### Display Package Items
```jsx
{package.items.map(item => (
  <li key={item.id}>{item.item_text}</li>
))}
```

### Gallery with Filter
```jsx
const [category, setCategory] = useState('all');
const url = category === 'all' 
  ? '/gallery/' 
  : `/gallery/?category=${category}`;
```

### Business Hours
```jsx
const hours = JSON.parse(contactInfo.business_hours);
Object.entries(hours).map(([day, time]) => ...)
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `uv sync` |
| Table doesn't exist | `uv run python cli.py init-db` |
| Old data format | `uv run python cli.py seed-db --clear` |
| Can't login | Check credentials: admin@lushmoments.com / Admin@123 |
| Email not sending | Check .env or check console (emails log there) |

---

## 📚 Documentation Files

1. **GETTING_STARTED.md** - Start here!
2. **API_ENDPOINTS.md** - Complete endpoint reference
3. **PROFESSIONAL_ENHANCEMENT.md** - Technical details
4. **QUICKSTART.md** - Original quick start
5. **CLI.md** - CLI commands

---

## ✅ Checklist for Production

- [ ] Change SECRET_KEY in .env
- [ ] Use strong admin password
- [ ] Configure SMTP for emails
- [ ] Switch to PostgreSQL
- [ ] Enable Redis for caching
- [ ] Set up SSL/TLS
- [ ] Configure CORS properly
- [ ] Set up backups
- [ ] Review security settings

---

## 💡 Pro Tips

1. **Use Swagger UI** at `/docs` for interactive testing
2. **Check terminal** for email output if SMTP not configured
3. **Restart server** to clear cache after data changes
4. **Use query params** for filtering (category, featured, status)
5. **Save admin token** for subsequent requests

---

**Quick Help:** Visit http://127.0.0.1:8000/docs for interactive API documentation

**Status:** ✅ Ready to use!
