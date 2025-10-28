"use client";

import type React from "react";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { motion } from "framer-motion";
import { Calendar, MapPin, Users, Sparkles, LogIn } from "lucide-react";
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { AnonymousChat } from "@/components/anonymous-chat";
import { useAuth } from "@/contexts/AuthContext";
import { AuthModal } from "@/components/auth-modal";
import { bookingApi, packageApi, type Package } from "@/lib/api";

export default function BookingPage() {
  const { toast } = useToast();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [packages, setPackages] = useState<Package[]>([]);
  const [formData, setFormData] = useState({
    eventType: "",
    eventDate: "",
    guestCount: "",
    venue: "",
    packageId: "",
    message: "",
  });

  // Load packages on mount
  useEffect(() => {
    const loadPackages = async () => {
      try {
        const data = await packageApi.getAll();
        setPackages(data);
      } catch (error) {
        console.error("Failed to load packages:", error);
      }
    };
    loadPackages();
  }, []);

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if user is authenticated
    if (!isAuthenticated) {
      toast({
        title: "Authentication Required",
        description: "Please login or create an account to book an event.",
        variant: "destructive",
      });
      setShowAuthModal(true);
      return;
    }

    setIsSubmitting(true);

    try {
      const bookingData = {
        event_type: formData.eventType,
        event_date: formData.eventDate,
        expected_guests: parseInt(formData.guestCount),
        venue_location: formData.venue,
        package_id: formData.packageId
          ? parseInt(formData.packageId)
          : undefined,
        additional_details: formData.message || undefined,
      };

      const response = await bookingApi.create(bookingData);

      toast({
        title: "Booking Request Received!",
        description: `Booking #${response.booking_id} created. We'll contact you within 24 hours.`,
      });

      // Reset form
      setFormData({
        eventType: "",
        eventDate: "",
        guestCount: "",
        venue: "",
        packageId: "",
        message: "",
      });
    } catch (error: any) {
      toast({
        title: "Booking Failed",
        description:
          error.message || "Failed to submit booking. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Show loading state while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" />
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
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
              Book Your Event
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Tell us about your celebration and we'll create a custom décor
              package that brings your vision to life.
            </p>
            {!isAuthenticated && (
              <Card className="bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800 mt-6">
                <CardContent className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <LogIn className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                    <p className="text-sm text-blue-900 dark:text-blue-100">
                      Please login to book an event
                    </p>
                  </div>
                  <Button
                    onClick={() => setShowAuthModal(true)}
                    size="sm"
                    variant="outline"
                    className="bg-white dark:bg-blue-900"
                  >
                    Login / Register
                  </Button>
                </CardContent>
              </Card>
            )}
          </motion.div>
        </div>
      </section>

      {/* Booking Form */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-3 gap-12">
            {/* Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="lg:col-span-2"
            >
              <Card>
                <CardHeader>
                  <h2 className="text-2xl font-[family-name:var(--font-display)]">
                    Event Details
                  </h2>
                  <p className="text-muted-foreground">
                    {isAuthenticated
                      ? `Welcome back, ${user?.name}! Fill out the form below.`
                      : "Please login to continue with your booking"}
                  </p>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* User Information Display */}
                    {isAuthenticated && user && (
                      <div className="space-y-4 p-4 bg-muted/50 rounded-lg">
                        <h3 className="font-semibold text-foreground">
                          Your Information
                        </h3>
                        <div className="grid sm:grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-muted-foreground">Name:</span>{" "}
                            <span className="font-medium">{user.name}</span>
                          </div>
                          <div>
                            <span className="text-muted-foreground">
                              Email:
                            </span>{" "}
                            <span className="font-medium">{user.email}</span>
                          </div>
                          {user.phone && (
                            <div>
                              <span className="text-muted-foreground">
                                Phone:
                              </span>{" "}
                              <span className="font-medium">{user.phone}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Event Information */}
                    <div className="space-y-4">
                      <h3 className="font-semibold text-foreground">
                        Event Information
                      </h3>
                      <div className="grid sm:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="eventType">Event Type *</Label>
                          <Select
                            value={formData.eventType}
                            onValueChange={(value) =>
                              handleChange("eventType", value)
                            }
                            disabled={!isAuthenticated}
                          >
                            <SelectTrigger id="eventType">
                              <SelectValue placeholder="Select event type" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="baby-shower">
                                Baby Shower
                              </SelectItem>
                              <SelectItem value="birthday">
                                Birthday Party
                              </SelectItem>
                              <SelectItem value="engagement">
                                Engagement Party
                              </SelectItem>
                              <SelectItem value="wedding">Wedding</SelectItem>
                              <SelectItem value="corporate">
                                Corporate Event
                              </SelectItem>
                              <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="eventDate">Event Date *</Label>
                          <Input
                            id="eventDate"
                            type="date"
                            value={formData.eventDate}
                            onChange={(e) =>
                              handleChange("eventDate", e.target.value)
                            }
                            disabled={!isAuthenticated}
                            required
                          />
                        </div>
                      </div>
                      <div className="grid sm:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="guestCount">
                            Expected Guest Count *
                          </Label>
                          <Input
                            id="guestCount"
                            type="number"
                            value={formData.guestCount}
                            onChange={(e) =>
                              handleChange("guestCount", e.target.value)
                            }
                            placeholder="50"
                            min="1"
                            disabled={!isAuthenticated}
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="packageId">Preferred Package</Label>
                          <Select
                            value={formData.packageId}
                            onValueChange={(value) =>
                              handleChange("packageId", value)
                            }
                            disabled={!isAuthenticated}
                          >
                            <SelectTrigger id="packageId">
                              <SelectValue placeholder="Select package" />
                            </SelectTrigger>
                            <SelectContent>
                              {packages.map((pkg) => (
                                <SelectItem
                                  key={pkg.id}
                                  value={pkg.id.toString()}
                                >
                                  {pkg.title} - ${pkg.price}
                                </SelectItem>
                              ))}
                              <SelectItem value="custom">
                                Custom Package
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="venue">Venue Location *</Label>
                        <Input
                          id="venue"
                          value={formData.venue}
                          onChange={(e) =>
                            handleChange("venue", e.target.value)
                          }
                          placeholder="123 Main St, City, State"
                          disabled={!isAuthenticated}
                          required
                        />
                      </div>
                    </div>

                    {/* Additional Details */}
                    <div className="space-y-4">
                      <h3 className="font-semibold text-foreground">
                        Additional Details
                      </h3>
                      <div className="space-y-2">
                        <Label htmlFor="message">
                          Tell us about your vision
                        </Label>
                        <Textarea
                          id="message"
                          value={formData.message}
                          onChange={(e) =>
                            handleChange("message", e.target.value)
                          }
                          placeholder="Share any specific themes, colors, or ideas you have in mind..."
                          rows={5}
                          disabled={!isAuthenticated}
                        />
                      </div>
                    </div>

                    <Button
                      type="submit"
                      size="lg"
                      className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
                      disabled={isSubmitting || !isAuthenticated}
                    >
                      {isSubmitting
                        ? "Submitting..."
                        : !isAuthenticated
                        ? "Login to Book"
                        : "Submit Booking Request"}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>

            {/* Sidebar Info */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-6"
            >
              <Card>
                <CardContent className="p-6 space-y-4">
                  <div className="flex items-start gap-3">
                    <Calendar className="h-5 w-5 text-primary flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-foreground mb-1">
                        Book in Advance
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        We recommend booking 4-6 weeks ahead for best
                        availability
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Users className="h-5 w-5 text-primary flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-foreground mb-1">
                        Free Consultation
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        Every booking includes a complimentary design
                        consultation
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <MapPin className="h-5 w-5 text-primary flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-foreground mb-1">
                        Service Area
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        We serve the greater metro area and surrounding regions
                      </p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <Sparkles className="h-5 w-5 text-primary flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-foreground mb-1">
                        Custom Packages
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        All packages can be customized to fit your vision and
                        budget
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-primary/10 to-accent/10 border-primary/20">
                <CardContent className="p-6 space-y-3">
                  <h3 className="font-semibold text-foreground">Need Help?</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Have questions about our services or packages? We're here to
                    help!
                  </p>
                  <Button
                    variant="outline"
                    className="w-full bg-transparent"
                    asChild
                  >
                    <a href="/contact">Contact Us</a>
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </section>

      <Footer />
      <AnonymousChat />
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        defaultTab="login"
      />
    </div>
  );
}
