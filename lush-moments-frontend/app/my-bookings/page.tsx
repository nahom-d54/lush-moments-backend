"use client";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { motion } from "framer-motion";
import {
  Calendar,
  MapPin,
  Users,
  Package,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { AnonymousChat } from "@/components/anonymous-chat";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { bookingApi, type Booking } from "@/lib/api";
import Link from "next/link";

const statusColors = {
  pending: "bg-yellow-500/10 text-yellow-700 border-yellow-500/20",
  confirmed: "bg-green-500/10 text-green-700 border-green-500/20",
  cancelled: "bg-red-500/10 text-red-700 border-red-500/20",
  completed: "bg-blue-500/10 text-blue-700 border-blue-500/20",
};

const statusLabels = {
  pending: "Pending",
  confirmed: "Confirmed",
  cancelled: "Cancelled",
  completed: "Completed",
};

export default function MyBookingsPage() {
  const { toast } = useToast();
  const { user } = useAuth();
  const router = useRouter();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      toast({
        title: "Authentication Required",
        description: "Please login to view your bookings",
        variant: "destructive",
      });
      router.push("/");
    }
  }, [user, router, toast]);

  useEffect(() => {
    const fetchBookings = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const data = await bookingApi.getMyBookings();
        setBookings(data);
      } catch (error: any) {
        toast({
          title: "Failed to Load Bookings",
          description: error.message || "Could not load your bookings",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, [user, toast]);

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-12 w-12 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary/5 via-background to-accent/5 py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center space-y-4 max-w-3xl mx-auto"
          >
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-[family-name:var(--font-display)] text-balance">
              My Bookings
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              View and manage your event booking requests
            </p>
          </motion.div>
        </div>
      </section>

      {/* Bookings Section */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : bookings.length === 0 ? (
            <div className="text-center py-20">
              <AlertCircle className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <p className="text-lg text-muted-foreground mb-6">
                You don't have any bookings yet.
              </p>
              <Button asChild>
                <Link href="/booking">Create Your First Booking</Link>
              </Button>
            </div>
          ) : (
            <div className="space-y-6">
              {bookings.map((booking, index) => (
                <motion.div
                  key={booking.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card className="hover:shadow-lg transition-shadow">
                    <CardHeader className="pb-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-xl font-semibold text-foreground mb-2">
                            {booking.event_type
                              .replace("-", " ")
                              .replace(/\b\w/g, (l) => l.toUpperCase())}
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            Booking #{booking.id} • Submitted on{" "}
                            {new Date(booking.created_at).toLocaleDateString()}
                          </p>
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium border ${
                            statusColors[
                              booking.status as keyof typeof statusColors
                            ] ||
                            "bg-gray-500/10 text-gray-700 border-gray-500/20"
                          }`}
                        >
                          {statusLabels[
                            booking.status as keyof typeof statusLabels
                          ] || booking.status}
                        </span>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="flex items-start gap-3">
                          <Calendar className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                          <div>
                            <p className="text-sm font-medium text-foreground">
                              Event Date
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {new Date(booking.event_date).toLocaleDateString(
                                "en-US",
                                {
                                  weekday: "long",
                                  year: "numeric",
                                  month: "long",
                                  day: "numeric",
                                }
                              )}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-start gap-3">
                          <Users className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                          <div>
                            <p className="text-sm font-medium text-foreground">
                              Guest Count
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {booking.expected_guests} guests
                            </p>
                          </div>
                        </div>

                        <div className="flex items-start gap-3">
                          <MapPin className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                          <div>
                            <p className="text-sm font-medium text-foreground">
                              Venue
                            </p>
                            <p className="text-sm text-muted-foreground line-clamp-2">
                              {booking.venue_location}
                            </p>
                          </div>
                        </div>

                        {booking.package_id && (
                          <div className="flex items-start gap-3">
                            <Package className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                            <div>
                              <p className="text-sm font-medium text-foreground">
                                Package
                              </p>
                              <p className="text-sm text-muted-foreground">
                                Package #{booking.package_id}
                              </p>
                            </div>
                          </div>
                        )}
                      </div>

                      {booking.additional_details && (
                        <div className="mt-4 pt-4 border-t border-border">
                          <p className="text-sm font-medium text-foreground mb-2">
                            Additional Details
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {booking.additional_details}
                          </p>
                        </div>
                      )}

                      {booking.admin_notes && (
                        <div className="mt-4 pt-4 border-t border-border bg-primary/5 -mx-6 px-6 py-4 rounded-b-lg">
                          <p className="text-sm font-medium text-foreground mb-2">
                            Admin Notes
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {booking.admin_notes}
                          </p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      {bookings.length > 0 && (
        <section className="py-16 lg:py-24 bg-gradient-to-br from-primary/10 via-background to-accent/10">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center space-y-6 max-w-2xl mx-auto"
            >
              <h2 className="text-3xl sm:text-4xl font-[family-name:var(--font-display)] text-balance">
                Planning Another Event?
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Create a new booking request and we'll help you bring your
                vision to life.
              </p>
              <Button
                asChild
                size="lg"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Link href="/booking">Create New Booking</Link>
              </Button>
            </motion.div>
          </div>
        </section>
      )}

      <Footer />
      <AnonymousChat />
    </div>
  );
}
