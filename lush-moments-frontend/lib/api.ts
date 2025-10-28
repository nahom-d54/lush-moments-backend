import { apiClient } from "./api-client";

// Types
export interface Booking {
  id: number;
  user_id: number;
  full_name: string;
  email: string;
  phone: string;
  event_type: string;
  event_date: string;
  expected_guests: number;
  venue_location: string;
  package_id?: number;
  additional_details?: string;
  special_requests?: string;
  status: string;
  created_at: string;
  updated_at?: string;
  admin_notes?: string;
}

export interface CreateBookingData {
  event_type: string;
  event_date: string;
  expected_guests: number;
  venue_location: string;
  package_id?: number;
  additional_details?: string;
  special_requests?: string;
  full_name?: string;
  email?: string;
  phone?: string;
}

export interface BookingResponse {
  message: string;
  booking_id: number;
  confirmation_email_sent: boolean;
}

export interface Package {
  id: number;
  title: string;
  description: string;
  price: number;
  is_popular: boolean;
  display_order: number;
  items: PackageItem[];
}

export interface PackageItem {
  id: number;
  package_id: number;
  item_text: string;
  display_order: number;
}

export interface GalleryItem {
  id: number;
  title: string;
  description: string;
  image_url: string;
  thumbnail_url?: string;
  category: string;
  tags?: string[];
  display_order: number;
  is_featured: boolean;
  created_at: string;
}

export interface GalleryList {
  items: GalleryItem[];
  total: number;
  category?: string;
}

export interface ContactMessage {
  full_name: string;
  email: string;
  phone_number?: string;
  message: string;
}

export interface ContactResponse {
  message: string;
  id: number;
}

export interface ContactInfo {
  email: string;
  phone: string;
  location: string;
  business_hours?: Record<string, string>;
  secondary_phone?: string;
  secondary_email?: string;
  facebook_url?: string;
  instagram_url?: string;
  twitter_url?: string;
  linkedin_url?: string;
  google_maps_url?: string;
}

// Booking API
export const bookingApi = {
  create: (data: CreateBookingData): Promise<BookingResponse> => {
    return apiClient.post<BookingResponse>("/bookings", data);
  },

  getMyBookings: (skip = 0, limit = 50): Promise<Booking[]> => {
    return apiClient.get<Booking[]>(`/bookings?skip=${skip}&limit=${limit}`);
  },

  getBooking: (id: number): Promise<Booking> => {
    return apiClient.get<Booking>(`/bookings/${id}`);
  },
};

// Package API
export const packageApi = {
  getAll: (): Promise<Package[]> => {
    return apiClient.get<Package[]>("/packages", false);
  },

  getById: (id: number): Promise<Package> => {
    return apiClient.get<Package>(`/packages/${id}`, false);
  },
};

// Gallery API
export const galleryApi = {
  getAll: (params?: {
    category?: string;
    featured_only?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<GalleryList> => {
    const query = new URLSearchParams();
    if (params?.category) query.append("category", params.category);
    if (params?.featured_only) query.append("featured_only", "true");
    if (params?.skip) query.append("skip", params.skip.toString());
    if (params?.limit) query.append("limit", params.limit.toString());

    const queryString = query.toString();
    return apiClient.get<GalleryList>(
      `/gallery/${queryString ? "?" + queryString : ""}`,
      false
    );
  },

  getCategories: (): Promise<{ categories: string[] }> => {
    return apiClient.get<{ categories: string[] }>(
      "/gallery/categories",
      false
    );
  },

  getById: (id: number): Promise<GalleryItem> => {
    return apiClient.get<GalleryItem>(`/gallery/${id}`, false);
  },
};

// Contact API
export const contactApi = {
  submit: (data: ContactMessage): Promise<ContactResponse> => {
    return apiClient.post<ContactResponse>("/contact/", data, false);
  },

  getInfo: (): Promise<ContactInfo> => {
    return apiClient.get<ContactInfo>("/contact-info/", false);
  },
};
