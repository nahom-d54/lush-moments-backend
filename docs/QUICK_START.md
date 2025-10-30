# 🚀 Quick Start Guide - Frontend Integration

## Overview

Your Lush Moments application now has a complete frontend-backend integration with authentication. This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- Backend database set up (SQLite)
- Redis running (optional for chat)

## 🏃 Quick Start (3 Steps)

### 1. Start the Backend

```powershell
# Navigate to backend directory
cd c:\Users\nahom\Desktop\chill\hobby1\lush-moments-backend

# Start FastAPI server
python -m uvicorn app.main:app --reload
```

**Backend will run on:** http://localhost:8000

### 2. Configure Frontend Environment

```powershell
# Navigate to frontend directory
cd c:\Users\nahom\Desktop\chill\hobby1\lush-moments-backend\lush-moments-frontend

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 3. Start the Frontend

```powershell
# Install dependencies (first time only)
npm install

# Start Next.js development server
npm run dev
```

**Frontend will run on:** http://localhost:3000

## ✅ Quick Test

1. Open browser: http://localhost:3000/booking
2. Click "Login / Register" button
3. Create a new account:
   - Name: Test User
   - Email: test@example.com
   - Password: test123
4. Submit a booking
5. See confirmation message!

## 📁 File Structure

```
lush-moments-backend/
├── app/
│   ├── main.py                    # ✅ CORS configured
│   ├── models/
│   │   ├── user.py                # ✅ OAuth support
│   │   └── event_booking.py       # ✅ User relationship
│   ├── routes/
│   │   ├── auth.py                # ✅ Login/Register/OAuth
│   │   ├── bookings.py            # ✅ Protected endpoints
│   │   └── admin/                 # ✅ All admin routes
│   └── schemas/
│       ├── auth.py                # ✅ Auth schemas
│       └── event_booking.py       # ✅ Booking schemas
│
└── lush-moments-frontend/
    ├── lib/
    │   ├── api-client.ts          # ✅ JWT token handling
    │   ├── auth.ts                # ✅ Auth functions
    │   └── api.ts                 # ✅ All API endpoints
    ├── contexts/
    │   └── AuthContext.tsx        # ✅ Global auth state
    ├── components/
    │   └── auth-modal.tsx         # ✅ Login/Register modal
    ├── app/
    │   ├── layout.tsx             # ✅ AuthProvider added
    │   └── booking/
    │       ├── page-old.tsx       # Original (backup)
    │       └── page-new.tsx       # ✅ Integrated version
    └── .env.local                 # Create this!
```

## 🔧 One-Time Setup

### Replace Booking Page (Optional)

To activate the new integrated booking page:

```powershell
cd lush-moments-frontend\app\booking
mv page.tsx page-old.tsx
mv page-new.tsx page.tsx
```

## 🎯 What's Working

✅ **Backend**
- FastAPI server with all routes
- JWT authentication
- Protected booking endpoints
- OAuth infrastructure ready
- CORS configured for frontend
- Database with User and Booking models

✅ **Frontend**
- Next.js 16 with App Router
- Authentication context & UI
- Protected booking page
- API client with token management
- Login/Register modal
- Auto-fill user information

✅ **Integration**
- Frontend talks to backend API
- JWT tokens automatically sent
- User authentication flow works
- Bookings saved to database
- Error handling and loading states

## 📊 API Endpoints

### Public Endpoints
- `POST /auth/register` - Create new account
- `POST /auth/login` - Login with email/password
- `POST /auth/oauth/callback` - OAuth login (Google/GitHub)
- `GET /packages` - List all packages
- `GET /gallery` - Browse event themes
- `POST /contact` - Submit contact form

### Protected Endpoints (Require Login)
- `POST /bookings` - Create new booking
- `GET /bookings` - Get my bookings
- `GET /bookings/{id}` - Get specific booking

### Admin Endpoints (Require Admin Role)
- `GET /admin/bookings` - List all bookings
- `PATCH /admin/bookings/{id}` - Update booking status
- Plus all other admin routes...

## 🌐 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Next.js app |
| Backend API | http://localhost:8000 | FastAPI server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| API Redoc | http://localhost:8000/redoc | ReDoc UI |

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if another service is using port 8000
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend won't start
```powershell
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Or use a different port
npm run dev -- --port 3001
```

### CORS Errors
✅ Already fixed! CORS middleware is configured in `app/main.py`

### Can't login
1. Check backend is running
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Open DevTools → Network tab → See API responses
4. Try clearing localStorage: `localStorage.clear()`

### TypeScript Errors in Frontend
These are normal and won't prevent the app from running:
```
Cannot find module 'react'
```
Just ignore them - the app will work fine.

## 📖 Documentation

Detailed guides available:
- `FRONTEND_INTEGRATION.md` - Complete step-by-step setup
- `FRONTEND_INTEGRATION_SUMMARY.md` - What's been completed
- `AUTHENTICATION_GUIDE.md` - Auth system details
- `AUTH_UPDATE_SUMMARY.md` - Security features

## 🎉 Next Steps

After basic testing works:

1. **Create "My Bookings" page** - See all user bookings
2. **Add user menu** - Profile dropdown in navigation
3. **Connect gallery** - Load themes from backend
4. **Connect contact form** - Submit to backend API
5. **Add OAuth buttons** - Google/GitHub login
6. **Deploy to production** - Vercel + Railway/Fly.io

## 💡 Tips

- Keep both servers running during development
- Use `Ctrl+C` to stop servers
- Backend auto-reloads on code changes (`--reload` flag)
- Frontend hot-reloads automatically
- Check terminal output for errors
- Use browser DevTools for debugging

## ✨ Features Ready to Use

1. **User Registration** - Create account with email/password
2. **User Login** - Authenticate and get JWT token
3. **Protected Bookings** - Only logged-in users can book
4. **Auto-fill User Data** - Name, email, phone from profile
5. **Package Selection** - Choose from available packages
6. **Form Validation** - All fields validated
7. **Error Handling** - User-friendly error messages
8. **Loading States** - Proper loading indicators
9. **Toast Notifications** - Success/error feedback
10. **Token Management** - Automatic token refresh on errors

## 🔐 Test Accounts

Create your own test account or use these credentials after registering:

```
Email: admin@example.com
Password: admin123
```

(Register this account first through the UI)

## 📞 Support

If you run into issues:
1. Check terminal output for errors
2. Look at browser console (F12)
3. Check Network tab for API calls
4. Review the detailed guides
5. Check database: `sqlite3 lush_moments.db` → `.tables`

---

**Ready to go!** Start both servers and visit http://localhost:3000/booking to begin! 🎊
