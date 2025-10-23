You are building the **FastAPI backend** for Lush Moments with:

### Tech Stack:
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM or Tortoise ORM
- JWT-based authentication (users + admin)
- Redis caching for faster responses
- WebSocket for real-time chat
- Background tasks for email notifications

### Core Models:
1. **User**
   - id, name, email, phone, role (admin/client)
2. **EventBooking**
   - id, client info, event_type, date, venue, package_id, message, status (pending/confirmed/completed)
3. **Package**
   - id, name, description, price, included_items
4. **Theme**
   - id, name, description, gallery_images
5. **Testimonial**
   - id, name, message, image_url, rating
6. **Session**
   - session_id, linked_user (nullable), created_at, chat_history
7. **ChatMessage**
   - id, session_id, sender_type (user/admin/bot), message, timestamp
8. **Translation**
   - content_type (Package/Theme/Category), object_id, language_code, field_name, translated_text

### API Endpoints:

**Public (Client)**
- `GET /packages`
- `GET /themes`
- `GET /testimonials`
- `POST /bookings` (creates new booking)
- `POST /sessions` (creates anonymous session)
- `POST /chat/connect` (WebSocket/SSE)

**Admin (Protected)**
- CRUD endpoints for packages, themes, gallery, testimonials
- `GET /bookings` (list all bookings)
- `PATCH /bookings/{id}` (update status)
- `GET /sessions` (list active chat sessions)
- `PATCH /sessions/{id}` (link anonymous session to user)
- `POST /chat/respond` (send messages as admin or AI)

### Features:
- Multi-language support: store translations in database
- Anonymous session tracking for users
- Real-time chat with admin
- Background tasks for email confirmations and notifications
- Media handling via Cloudinary or local storage
- Docker-ready deployment (Dockerfile + docker-compose)
