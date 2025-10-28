import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  galleryApi,
  packageApi,
  bookingApi,
  contactApi,
  type GalleryItem,
  type Package,
  type Booking,
  type CreateBookingData,
  type ContactMessage,
  type ContactInfo,
} from "@/lib/api";

// Query Keys
export const queryKeys = {
  gallery: {
    all: ["gallery"] as const,
    list: (category?: string) => ["gallery", category || "all"] as const,
    detail: (id: number) => ["gallery", id] as const,
    categories: ["gallery", "categories"] as const,
  },
  packages: {
    all: ["packages"] as const,
    detail: (id: number) => ["packages", id] as const,
  },
  bookings: {
    all: ["bookings"] as const,
    list: (skip?: number, limit?: number) =>
      ["bookings", "list", skip, limit] as const,
    detail: (id: number) => ["bookings", id] as const,
  },
  contact: {
    info: ["contact", "info"] as const,
  },
};

// Gallery Hooks
export function useGalleryItems(category?: string) {
  return useQuery({
    queryKey: queryKeys.gallery.list(category),
    queryFn: () =>
      galleryApi.getAll({
        category: category === "all" ? undefined : category,
        limit: 50,
      }),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  });
}

export function useGalleryItem(id: number) {
  return useQuery({
    queryKey: queryKeys.gallery.detail(id),
    queryFn: () => galleryApi.getById(id),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  });
}

export function useGalleryCategories() {
  return useQuery({
    queryKey: queryKeys.gallery.categories,
    queryFn: () => galleryApi.getCategories(),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  });
}

// Package Hooks
export function usePackages() {
  return useQuery({
    queryKey: queryKeys.packages.all,
    queryFn: () => packageApi.getAll(),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  });
}

export function usePackage(id: number) {
  return useQuery({
    queryKey: queryKeys.packages.detail(id),
    queryFn: () => packageApi.getById(id),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
    enabled: !!id,
  });
}

// Booking Hooks
export function useMyBookings(skip = 0, limit = 50) {
  return useQuery({
    queryKey: queryKeys.bookings.list(skip, limit),
    queryFn: () => bookingApi.getMyBookings(skip, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes (bookings change more frequently)
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useBooking(id: number) {
  return useQuery({
    queryKey: queryKeys.bookings.detail(id),
    queryFn: () => bookingApi.getBooking(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    enabled: !!id,
  });
}

// Booking Mutations
export function useCreateBooking() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateBookingData) => bookingApi.create(data),
    onSuccess: () => {
      // Invalidate and refetch bookings list
      queryClient.invalidateQueries({ queryKey: queryKeys.bookings.all });
    },
  });
}

// Contact Hooks
export function useContactInfo() {
  return useQuery({
    queryKey: queryKeys.contact.info,
    queryFn: () => contactApi.getInfo(),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    gcTime: 24 * 60 * 60 * 1000, // 24 hours
  });
}

export function useSubmitContact() {
  return useMutation({
    mutationFn: (data: ContactMessage) => contactApi.submit(data),
  });
}
