# 🎯 API Endpoints Summary - Professional Event Management Platform

## Base URL: `http://127.0.0.1:8000`

---

## 🌐 Public Endpoints (No Authentication Required)

### Packages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/packages` | Get all packages with bullet point items |
| GET | `/packages/{id}` | Get specific package details |

**Query Parameters:**
- `lang` - Language code (e.g., 'es', 'fr')

**Response includes:**
```json
{
  "title": "Classic Package",
  "description": "...",
  "price": 1200.0,
  "is_popular": true,
  "items": [
    {"item_text": "Venue for up to 100 guests"},
    {"item_text": "Full catering with 5 meal options"}
  ]
}
```

---

### Contact Form
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/contact/` | Submit contact form (Get in Touch) |

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+1-555-1234",
  "message": "I need information about wedding packages"
}
```

**Response:**
```json
{
  "message": "Thank you for contacting us! We'll get back to you soon.",
  "id": 1
}
```

**Features:**
- ✅ Sends confirmation email to user
- ✅ Sends notification email to admin
- ✅ Beautiful HTML email templates

---

### Gallery
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/gallery/` | Browse gallery items |
| GET | `/gallery/categories` | Get all unique categories |
| GET | `/gallery/{id}` | Get specific gallery item |

**Query Parameters for `/gallery/`:**
- `category` - Filter by category (wedding, birthday, corporate, etc.)
- `featured_only` - Show only featured items (true/false)
- `skip` - Pagination offset
- `limit` - Items per page

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Elegant Wedding Reception",
      "description": "Beautiful setup...",
      "image_url": "/uploads/gallery/wedding1.jpg",
      "thumbnail_url": "/uploads/gallery/thumbs/wedding1.jpg",
      "category": "wedding",
      "tags": "[\"elegant\", \"romantic\"]",
      "is_featured": true,
      "created_at": "2025-10-23T12:00:00"
    }
  ],
  "total": 5,
  "category": "wedding"
}
```

---

### Contact Information
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/contact-info/` | Get business contact information |

**Response:**
```json
{
  "id": 1,
  "email": "info@lushmoments.com",
  "phone": "+1-555-LUSH-MOMENTS",
  "location": "123 Event Plaza, Suite 456, Los Angeles, CA 90001",
  "business_hours": "{\"monday\":\"9:00 AM - 6:00 PM\"...}",
  "secondary_phone": "+1-555-EVENT-NOW",
  "secondary_email": "bookings@lushmoments.com",
  "facebook_url": "https://facebook.com/lushmoments",
  "instagram_url": "https://instagram.com/lushmoments",
  "twitter_url": "https://twitter.com/lushmoments",
  "linkedin_url": "https://linkedin.com/company/lushmoments",
  "google_maps_url": "https://maps.google.com/?q=..."
}
```

---

### Bookings
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bookings` | Create event booking |
| GET | `/bookings/{id}` | Get specific booking |

**Request Body for POST:**
```json
{
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1-555-5678",
  "event_type": "Wedding",
  "event_date": "2025-06-15T14:00:00",
  "expected_guests": 150,
  "venue_location": "Grand Ballroom, Downtown",
  "package_id": 2,
  "additional_details": "Outdoor ceremony with indoor reception",
  "special_requests": "Vegetarian menu options for 20 guests"
}
```

**Event Type Options:**
- Wedding
- Birthday
- Anniversary
- Corporate
- Conference
- Gala
- Fundraiser
- Graduation
- Other

**Response:**
```json
{
  "message": "Your booking request has been submitted successfully!",
  "booking_id": 4,
  "confirmation_email_sent": true
}
```

**Features:**
- ✅ Sends confirmation email to customer
- ✅ Sends notification email to admin
- ✅ Professional email templates with booking details

---

### Themes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/themes` | Get all event themes |
| GET | `/themes/{id}` | Get specific theme |

---

### Testimonials
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/testimonials` | Get all testimonials |
| GET | `/testimonials/{id}` | Get specific testimonial |

---

## 🔐 Admin Endpoints (Authentication Required)

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Admin login |
| POST | `/auth/register` | Register new user (returns 403 for non-admins) |

**Login Request:**
```json
{
  "email": "admin@lushmoments.com",
  "password": "Admin@123"
}
```

**Login Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Use token in subsequent requests:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

### Admin - Contact Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/contact/messages` | Get all contact messages |
| GET | `/contact/messages/{id}` | Get specific message |
| PATCH | `/contact/messages/{id}` | Mark as read/responded |
| DELETE | `/contact/messages/{id}` | Delete message |

**Query Parameters for GET `/contact/messages`:**
- `unread_only` - Filter unread messages (true/false)
- `skip` - Pagination offset
- `limit` - Messages per page

**PATCH Request Body:**
```json
{
  "is_read": true,
  "responded_at": "2025-10-23T15:30:00"
}
```

---

### Admin - Gallery Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/gallery/` | Upload new gallery item |
| PATCH | `/gallery/{id}` | Update gallery item |
| DELETE | `/gallery/{id}` | Delete gallery item |

**POST Request Body:**
```json
{
  "title": "Corporate Event 2024",
  "description": "Annual company gala",
  "image_url": "/uploads/gallery/corporate1.jpg",
  "thumbnail_url": "/uploads/gallery/thumbs/corporate1.jpg",
  "category": "corporate",
  "tags": "[\"professional\", \"modern\"]",
  "display_order": 0,
  "is_featured": true
}
```

**PATCH Request Body (all fields optional):**
```json
{
  "title": "Updated Title",
  "is_featured": false,
  "display_order": 5
}
```

---

### Admin - Contact Info Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/contact-info/` | Create contact info (one-time setup) |
| PATCH | `/contact-info/` | Update contact information |
| DELETE | `/contact-info/` | Delete contact info |

**POST/PATCH Request Body:**
```json
{
  "email": "info@lushmoments.com",
  "phone": "+1-555-LUSH-MOMENTS",
  "location": "123 Event Plaza, LA, CA 90001",
  "business_hours": "{\"monday\":\"9:00 AM - 6:00 PM\"...}",
  "facebook_url": "https://facebook.com/lushmoments",
  "instagram_url": "https://instagram.com/lushmoments"
}
```

---

### Admin - Package Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/packages/` | Get all packages |
| POST | `/admin/packages/` | Create new package |
| GET | `/admin/packages/{id}` | Get specific package |
| PATCH | `/admin/packages/{id}` | Update package |
| DELETE | `/admin/packages/{id}` | Delete package |

**POST Request Body:**
```json
{
  "title": "New Package",
  "description": "Custom event package",
  "price": 1500.0,
  "is_popular": false,
  "display_order": 5,
  "items": [
    "Venue for up to 75 guests",
    "Catering with 4 meal options",
    "Standard decoration package",
    "4 hours event time"
  ]
}
```

**PATCH Request Body (all fields optional):**
```json
{
  "title": "Updated Package",
  "price": 1600.0,
  "is_popular": true,
  "items": [
    "Updated item 1",
    "Updated item 2"
  ]
}
```

---

### Admin - Booking Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bookings` | Get all bookings |
| PATCH | `/bookings/{id}` | Update booking status/notes |

**Query Parameters for GET `/bookings`:**
- `status` - Filter by status (pending, confirmed, completed, cancelled)
- `skip` - Pagination offset
- `limit` - Bookings per page

**PATCH Request Body:**
```json
{
  "status": "confirmed",
  "admin_notes": "Deposit received. Confirmed via phone call on Oct 23."
}
```

**Booking Statuses:**
- `pending` - New booking, awaiting review
- `confirmed` - Booking confirmed, deposit received
- `completed` - Event completed successfully
- `cancelled` - Booking cancelled

---

### Admin - Theme Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/themes/` | Get all themes |
| POST | `/admin/themes/` | Create new theme |
| GET | `/admin/themes/{id}` | Get specific theme |
| PUT | `/admin/themes/{id}` | Update theme |
| DELETE | `/admin/themes/{id}` | Delete theme |

---

### Admin - Testimonial Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/testimonials/` | Get all testimonials |
| POST | `/admin/testimonials/` | Create new testimonial |
| GET | `/admin/testimonials/{id}` | Get specific testimonial |
| PUT | `/admin/testimonials/{id}` | Update testimonial |
| DELETE | `/admin/testimonials/{id}` | Delete testimonial |

---

### Admin - Translation Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/translations/` | Get all translations |
| POST | `/admin/translations/` | Create new translation |
| GET | `/admin/translations/{id}` | Get specific translation |
| PUT | `/admin/translations/{id}` | Update translation |
| DELETE | `/admin/translations/{id}` | Delete translation |

---

## 🔧 Utility Endpoints

### Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API health status |

**Response:**
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "0.1.0"
}
```

### Root
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |

---

## 📊 Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

---

## 🎨 Frontend Integration Examples

### React - Submit Contact Form
```jsx
const submitContactForm = async (formData) => {
  const response = await fetch('http://127.0.0.1:8000/contact/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });
  
  const result = await response.json();
  console.log(result.message); // Thank you message
};
```

### React - Fetch and Display Packages
```jsx
const fetchPackages = async () => {
  const response = await fetch('http://127.0.0.1:8000/packages');
  const packages = await response.json();
  
  return packages.map(pkg => (
    <div key={pkg.id}>
      <h3>{pkg.title}</h3>
      <p>{pkg.description}</p>
      <p>${pkg.price}</p>
      <ul>
        {pkg.items.map(item => (
          <li key={item.id}>{item.item_text}</li>
        ))}
      </ul>
    </div>
  ));
};
```

### React - Gallery with Filters
```jsx
const GalleryComponent = () => {
  const [category, setCategory] = useState('all');
  
  const fetchGallery = async () => {
    const url = category === 'all' 
      ? 'http://127.0.0.1:8000/gallery/'
      : `http://127.0.0.1:8000/gallery/?category=${category}`;
    
    const response = await fetch(url);
    const data = await response.json();
    return data.items;
  };
  
  // Use in component...
};
```

### React - Create Booking
```jsx
const createBooking = async (bookingData) => {
  const response = await fetch('http://127.0.0.1:8000/bookings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookingData),
  });
  
  const result = await response.json();
  if (response.ok) {
    alert(result.message); // Success message
  }
};
```

### React - Admin Operations (with Auth)
```jsx
// Login first
const login = async (email, password) => {
  const response = await fetch('http://127.0.0.1:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  
  const { access_token } = await response.json();
  localStorage.setItem('token', access_token);
  return access_token;
};

// Use token for admin requests
const getContactMessages = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://127.0.0.1:8000/contact/messages', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return await response.json();
};
```

---

## 📖 Additional Resources

- **Full API Documentation:** http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs:** http://127.0.0.1:8000/redoc (ReDoc)
- **Technical Documentation:** See `PROFESSIONAL_ENHANCEMENT.md`
- **Getting Started Guide:** See `GETTING_STARTED.md`
- **CLI Commands:** See `CLI.md`

---

## 💡 Tips

1. **Use Swagger UI** at `/docs` to test all endpoints interactively
2. **Check email console output** if SMTP is not configured (emails log to terminal)
3. **Refresh cache** by restarting server after data changes
4. **Use query parameters** for filtering and pagination
5. **Include Authorization header** for all admin endpoints

---

**API Version:** 2.0.0 - Professional Enhancement  
**Last Updated:** October 23, 2025  
**Status:** ✅ Production Ready
