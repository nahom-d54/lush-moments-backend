# TanStack Query Setup - Complete

## Installation

Install TanStack Query:

```bash
npm install @tanstack/react-query
```

Or if using pnpm (you may need to enable scripts first):

```bash
pnpm add @tanstack/react-query
```

## What was implemented:

### 1. **Created `contexts/QueryProvider.tsx`**
   - Global QueryClient with 24-hour default cache configuration
   - Disabled unnecessary refetches for optimal performance

### 2. **Updated `app/layout.tsx`**
   - Added QueryProvider to wrap the entire application
   - All pages now have access to TanStack Query

### 3. **Created `hooks/use-api-queries.ts`**
   - Custom hooks for all API endpoints
   - Centralized query keys for easy cache management
   - Proper TypeScript types for all queries

### 4. **Updated Pages to use TanStack Query:**

   #### **Gallery Page** (`app/gallery/page.tsx`)
   - Uses `useGalleryItems(category)` hook
   - Caches gallery data for 24 hours per category
   - Automatic background refetching disabled

   #### **Packages Page** (`app/packages/page.tsx`)
   - Uses `usePackages()` hook
   - Caches package data for 24 hours
   - Instant loading on subsequent visits

   #### **Contact Page** (`app/contact/page.tsx`)
   - Uses `useContactInfo()` for contact information
   - Uses `useSubmitContact()` mutation for form submission
   - Contact info cached for 24 hours

## Available Custom Hooks:

### Gallery Hooks
- `useGalleryItems(category?)` - Get all gallery items (filtered by category)
- `useGalleryItem(id)` - Get single gallery item
- `useGalleryCategories()` - Get available categories

### Package Hooks
- `usePackages()` - Get all packages
- `usePackage(id)` - Get single package

### Booking Hooks
- `useMyBookings(skip?, limit?)` - Get user's bookings (5 min cache)
- `useBooking(id)` - Get single booking (5 min cache)
- `useCreateBooking()` - Mutation to create booking

### Contact Hooks
- `useContactInfo()` - Get contact information (24 hour cache)
- `useSubmitContact()` - Mutation to submit contact form

## Cache Configuration:

### Long-term caching (24 hours):
- Gallery items
- Packages
- Contact information
- Categories

### Short-term caching (5 minutes):
- Bookings (more dynamic data)

### No caching:
- Form submissions (mutations)

## Query Keys Structure:

```typescript
queryKeys.gallery.all          // ["gallery"]
queryKeys.gallery.list(cat)    // ["gallery", "all"] or ["gallery", "Birthdays"]
queryKeys.gallery.detail(1)    // ["gallery", 1]

queryKeys.packages.all         // ["packages"]
queryKeys.packages.detail(1)   // ["packages", 1]

queryKeys.bookings.all         // ["bookings"]
queryKeys.bookings.list()      // ["bookings", "list", skip, limit]
queryKeys.bookings.detail(1)   // ["bookings", 1]

queryKeys.contact.info         // ["contact", "info"]
```

## Benefits:

✅ **Reduced API Calls** - Data cached for 24 hours significantly reduces backend load
✅ **Better Performance** - Instant page loads when data is cached
✅ **Automatic Cache Management** - TanStack Query handles invalidation and garbage collection
✅ **Optimistic Updates** - Mutations can invalidate related queries automatically
✅ **Type Safety** - Full TypeScript support with proper types
✅ **Developer Experience** - Clean, reusable hooks for all API calls

## Next Steps to Implement:

1. Install the package: `npm install @tanstack/react-query`
2. Update booking page to use `useCreateBooking()` mutation
3. Add React Query DevTools for development (optional):
   ```bash
   npm install @tanstack/react-query-devtools
   ```

## Example Usage:

```tsx
// In any component
import { useGalleryItems, usePackages } from "@/hooks/use-api-queries";

function MyComponent() {
  const { data, isLoading, error } = useGalleryItems("Birthdays");
  
  if (isLoading) return <Spinner />;
  if (error) return <Error />;
  
  return <div>{data?.items.map(...)}</div>;
}
```

