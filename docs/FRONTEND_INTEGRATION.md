# Frontend-Backend Integration Guide

This guide will help you complete the integration between the Lush Moments Next.js frontend and FastAPI backend.

## Prerequisites

Make sure both projects are set up:
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000

## Step 1: Install Required Frontend Packages

Navigate to the frontend directory and install the missing dependencies:

```powershell
cd lush-moments-frontend
npm install axios
```

Optional OAuth packages (for future use):
```powershell
npm install @react-oauth/google
```

## Step 2: Configure Environment Variables

Create `.env.local` in the frontend root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
NEXT_PUBLIC_GITHUB_CLIENT_ID=your-github-client-id
```

## Step 3: Update Backend CORS Settings

In your FastAPI backend, update `main.py` to allow frontend requests:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Lush Moments API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development
        "http://127.0.0.1:3000",
        # Add production URLs when deploying
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 4: Replace Booking Page

Replace the existing booking page with the new integrated version:

```powershell
# Backup the original
cd app\booking
mv page.tsx page-old.tsx

# Use the new integrated version
mv page-new.tsx page.tsx
```

## Step 5: Update Navigation Component

The navigation component needs to show authentication state. Create `components/user-menu.tsx`:

```tsx
'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { User, LogOut, Calendar } from 'lucide-react'
import Link from 'next/link'

export function UserMenu() {
  const { user, isAuthenticated, logout } = useAuth()

  if (!isAuthenticated || !user) {
    return null
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          {user.avatar_url ? (
            <img
              src={user.avatar_url}
              alt={user.name}
              className="h-8 w-8 rounded-full"
            />
          ) : (
            <User className="h-5 w-5" />
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{user.name}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {user.email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href="/my-bookings">
            <Calendar className="mr-2 h-4 w-4" />
            My Bookings
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={logout}>
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

## Step 6: Create My Bookings Page

Create `app/my-bookings/page.tsx`:

```tsx
'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { bookingApi, type Booking } from '@/lib/api'
import { Navigation } from '@/components/navigation'
import { Footer } from '@/components/footer'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Calendar, MapPin, Users, Package } from 'lucide-react'

export default function MyBookingsPage() {
  const { isAuthenticated, isLoading, user } = useAuth()
  const router = useRouter()
  const [bookings, setBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/booking')
    }
  }, [isAuthenticated, isLoading, router])

  useEffect(() => {
    if (isAuthenticated) {
      loadBookings()
    }
  }, [isAuthenticated])

  const loadBookings = async () => {
    try {
      const data = await bookingApi.getMyBookings()
      setBookings(data)
    } catch (error) {
      console.error('Failed to load bookings:', error)
    } finally {
      setLoading(false)
    }
  }

  if (isLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <Navigation />
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold mb-8">My Bookings</h1>
        
        {bookings.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <p className="text-muted-foreground">No bookings yet</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {bookings.map((booking) => (
              <Card key={booking.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold capitalize">
                      {booking.event_type.replace('-', ' ')}
                    </h2>
                    <Badge>{booking.status}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <span>{new Date(booking.event_date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      <span>{booking.expected_guests} guests</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-muted-foreground" />
                      <span>{booking.venue_location}</span>
                    </div>
                    {booking.package_id && (
                      <div className="flex items-center gap-2">
                        <Package className="h-4 w-4 text-muted-foreground" />
                        <span>Package #{booking.package_id}</span>
                      </div>
                    )}
                  </div>
                  {booking.additional_details && (
                    <div className="mt-4 p-4 bg-muted rounded-lg">
                      <p className="text-sm">{booking.additional_details}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  )
}
```

## Step 7: Test the Integration

### Start the Backend
```powershell
cd lush-moments-backend
python -m uvicorn app.main:app --reload
```

### Start the Frontend
```powershell
cd lush-moments-frontend
npm run dev
```

### Test Flow:
1. Visit http://localhost:3000/booking
2. Try to submit a booking (should prompt for login)
3. Click "Login / Register" and create an account
4. Fill out the booking form
5. Submit the booking
6. Visit "My Bookings" to see your bookings

## Files Created/Modified

### New Files:
- `lib/api-client.ts` - API client with JWT token handling
- `lib/auth.ts` - Authentication API functions
- `lib/api.ts` - All API endpoints (bookings, gallery, packages, contact)
- `contexts/AuthContext.tsx` - Authentication context provider
- `components/auth-modal.tsx` - Login/Register modal
- `components/user-menu.tsx` - User dropdown menu
- `app/my-bookings/page.tsx` - User bookings list page
- `.env.local.example` - Environment variable template

### Modified Files:
- `app/layout.tsx` - Added AuthProvider
- `app/booking/page.tsx` - Integrated with backend, requires authentication
- Backend `app/main.py` - Updated CORS settings

## Features Implemented

✅ JWT-based authentication
✅ User registration and login
✅ Protected booking endpoints
✅ Automatic user data filling
✅ My Bookings page
✅ User menu with profile
✅ OAuth infrastructure (ready for Google/GitHub)
✅ Error handling and loading states
✅ Token storage in localStorage

## Next Steps

1. **Add OAuth Buttons**: Implement Google/GitHub login
2. **Gallery Integration**: Connect gallery page to backend
3. **Contact Form**: Connect contact page to backend
4. **Admin Panel**: Create admin dashboard (optional)
5. **Email Notifications**: Set up email confirmations
6. **Deployment**: Deploy to production

## Troubleshooting

### CORS Errors
- Make sure backend CORS middleware includes frontend URL
- Check that `allow_credentials=True` is set

### Authentication Issues
- Clear localStorage: `localStorage.clear()`
- Check token format in Network tab
- Verify JWT secret matches between frontend and backend

### API Connection Errors
- Verify backend is running on port 8000
- Check `.env.local` has correct API_URL
- Look for errors in browser console and terminal

## API Documentation

All backend endpoints are documented at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Support

For issues or questions:
- Check backend logs for error messages
- Use browser DevTools Network tab to debug API calls
- Review the authentication guide: `AUTHENTICATION_GUIDE.md`
