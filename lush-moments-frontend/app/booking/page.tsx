"use client";

import type React from "react";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { motion } from "framer-motion";
import {
  Calendar,
  MapPin,
  Users,
  Sparkles,
  Loader2,
  Plus,
  X,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { useEnhancements } from "@/hooks/use-api-queries";
import { AnonymousChat } from "@/components/anonymous-chat";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter, useSearchParams } from "next/navigation";
import {
  bookingApi,
  packageApi,
  type Package,
  type PackageEnhancement,
  type EnhancementSelection,
} from "@/lib/api";

export default function BookingPage() {
  const { toast } = useToast();
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const packageParam = searchParams.get("package");

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [packages, setPackages] = useState<Package[]>([]);
  const [loadingPackages, setLoadingPackages] = useState(true);
  const [selectedEnhancements, setSelectedEnhancements] = useState<
    Map<string, { enhancement: PackageEnhancement; quantity: number }>
  >(new Map());
  const { data: enhancements, isLoading: loadingEnhancements } =
    useEnhancements();

  const [formData, setFormData] = useState({
    name: user?.name || "",
    email: user?.email || "",
    phone: user?.phone || "",
    eventType: "",
    eventDate: "",
    guestCount: "",
    venue: "",
    packageType: packageParam || "",
    message: "",
  });

  // Redirect to auth if not logged in
  useEffect(() => {
    if (!authLoading && !user) {
      toast({
        title: "Authentication Required",
        description:
          "Please login or create an account before booking an event.",
        variant: "destructive",
      });

      // Redirect to auth page with return URL
      router.push(
        `/auth?mode=login&redirect=/booking${
          packageParam ? `?package=${packageParam}` : ""
        }`
      );
    }
  }, [user, authLoading, router, toast, packageParam]);

  useEffect(() => {
    const fetchPackages = async () => {
      try {
        const data = await packageApi.getAll();
        setPackages(data);
      } catch (error) {
        console.error("Failed to load packages:", error);
      } finally {
        setLoadingPackages(false);
      }
    };

    fetchPackages();
  }, []);

  useEffect(() => {
    if (user) {
      setFormData((prev) => ({
        ...prev,
        name: user.name || "",
        email: user.email || "",
        phone: user.phone || "",
      }));
    }
  }, [user]);

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const addEnhancement = (enhancement: PackageEnhancement) => {
    setSelectedEnhancements((prev) => {
      const newMap = new Map(prev);
      const existing = newMap.get(enhancement.id);
      if (existing) {
        newMap.set(enhancement.id, {
          enhancement,
          quantity: existing.quantity + 1,
        });
      } else {
        newMap.set(enhancement.id, { enhancement, quantity: 1 });
      }
      return newMap;
    });
  };

  const removeEnhancement = (enhancementId: string) => {
    setSelectedEnhancements((prev) => {
      const newMap = new Map(prev);
      newMap.delete(enhancementId);
      return newMap;
    });
  };

  const updateEnhancementQuantity = (
    enhancementId: string,
    quantity: number
  ) => {
    if (quantity < 1) {
      removeEnhancement(enhancementId);
      return;
    }
    setSelectedEnhancements((prev) => {
      const newMap = new Map(prev);
      const existing = newMap.get(enhancementId);
      if (existing) {
        newMap.set(enhancementId, { ...existing, quantity });
      }
      return newMap;
    });
  };

  const calculateEnhancementsTotal = () => {
    let total = 0;
    selectedEnhancements.forEach(({ enhancement, quantity }) => {
      total += enhancement.starting_price * quantity;
    });
    return total;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Build enhancements array
      const enhancements: EnhancementSelection[] = Array.from(
        selectedEnhancements.values()
      ).map(({ enhancement, quantity }) => ({
        enhancement_id: enhancement.id,
        quantity,
      }));

      const bookingData = {
        event_type: formData.eventType,
        event_date: formData.eventDate,
        expected_guests: parseInt(formData.guestCount),
        venue_location: formData.venue,
        package_id: formData.packageType || undefined,
        additional_details: formData.message || undefined,
        enhancements: enhancements.length > 0 ? enhancements : undefined,
        // If user is not authenticated, include contact details
        ...(!user && {
          full_name: formData.name,
          email: formData.email,
          phone: formData.phone,
        }),
      };

      const response = await bookingApi.create(bookingData);

      toast({
        title: "Booking Request Received!",
        description:
          "We'll get back to you within 24 hours to discuss your event details.",
      });

      // Reset form
      setFormData({
        name: user?.name || "",
        email: user?.email || "",
        phone: user?.phone || "",
        eventType: "",
        eventDate: "",
        guestCount: "",
        venue: "",
        packageType: "",
        message: "",
      });
      setSelectedEnhancements(new Map());

      // Redirect to bookings page if authenticated
      if (user) {
        setTimeout(() => router.push("/my-bookings"), 2000);
      }
    } catch (error: any) {
      toast({
        title: "Booking Failed",
        description:
          error.message ||
          "Could not submit booking request. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Navigation />

      {/* Show loading state while checking authentication */}
      {authLoading ? (
        <section className="py-24">
          <div className="container mx-auto px-4 text-center">
            <Loader2 className="h-12 w-12 animate-spin mx-auto text-primary" />
            <p className="mt-4 text-muted-foreground">
              Checking authentication...
            </p>
          </div>
        </section>
      ) : user ? (
        <>
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
                        Fill out the form below and we'll get back to you
                        shortly
                      </p>
                    </CardHeader>
                    <CardContent>
                      <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Personal Information */}
                        <div className="space-y-4">
                          <h3 className="font-semibold text-foreground">
                            Your Information
                          </h3>
                          <div className="grid sm:grid-cols-2 gap-4">
                            <div className="space-y-2">
                              <Label htmlFor="name">Full Name *</Label>
                              <Input
                                id="name"
                                value={formData.name}
                                onChange={(e) =>
                                  handleChange("name", e.target.value)
                                }
                                placeholder="John Doe"
                                required
                              />
                            </div>
                            <div className="space-y-2">
                              <Label htmlFor="email">Email *</Label>
                              <Input
                                id="email"
                                type="email"
                                value={formData.email}
                                onChange={(e) =>
                                  handleChange("email", e.target.value)
                                }
                                placeholder="john@example.com"
                                required
                              />
                            </div>
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="phone">Phone Number *</Label>
                            <Input
                              id="phone"
                              type="tel"
                              value={formData.phone}
                              onChange={(e) =>
                                handleChange("phone", e.target.value)
                              }
                              placeholder="+1 (555) 123-4567"
                              required
                            />
                          </div>
                        </div>

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
                                  <SelectItem value="wedding">
                                    Wedding
                                  </SelectItem>
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
                                required
                              />
                            </div>
                            <div className="space-y-2">
                              <Label htmlFor="packageType">
                                Preferred Package
                              </Label>
                              <Select
                                value={formData.packageType}
                                onValueChange={(value) =>
                                  handleChange("packageType", value)
                                }
                                disabled={loadingPackages}
                              >
                                <SelectTrigger id="packageType">
                                  <SelectValue
                                    placeholder={
                                      loadingPackages
                                        ? "Loading packages..."
                                        : "Select package"
                                    }
                                  />
                                </SelectTrigger>
                                <SelectContent>
                                  {packages.map((pkg) => (
                                    <SelectItem
                                      key={pkg.id}
                                      value={pkg.id.toString()}
                                    >
                                      {pkg.title} - $
                                      {pkg.price.toLocaleString()}
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
                              required
                            />
                          </div>
                        </div>

                        {/* Package Enhancements */}
                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <h3 className="font-semibold text-foreground">
                              Package Enhancements
                            </h3>
                            {selectedEnhancements.size > 0 && (
                              <Badge variant="secondary">
                                {selectedEnhancements.size} selected
                              </Badge>
                            )}
                          </div>

                          {/* Selected Enhancements */}
                          {selectedEnhancements.size > 0 && (
                            <div className="space-y-2 p-4 bg-muted/50 rounded-lg">
                              <p className="text-sm font-medium">Selected:</p>
                              {Array.from(selectedEnhancements.values()).map(
                                ({ enhancement, quantity }) => (
                                  <div
                                    key={enhancement.id}
                                    className="flex items-center justify-between gap-2 text-sm bg-background p-2 rounded border"
                                  >
                                    <div className="flex-1">
                                      <p className="font-medium">
                                        {enhancement.name}
                                      </p>
                                      <p className="text-xs text-muted-foreground">
                                        ${enhancement.starting_price} each
                                      </p>
                                    </div>
                                    <div className="flex items-center gap-2">
                                      <Input
                                        type="number"
                                        min="1"
                                        value={quantity}
                                        onChange={(e) =>
                                          updateEnhancementQuantity(
                                            enhancement.id,
                                            parseInt(e.target.value) || 1
                                          )
                                        }
                                        className="w-16 h-8"
                                      />
                                      <span className="text-sm font-medium min-w-[60px]">
                                        ${enhancement.starting_price * quantity}
                                      </span>
                                      <Button
                                        type="button"
                                        variant="ghost"
                                        size="sm"
                                        onClick={() =>
                                          removeEnhancement(enhancement.id)
                                        }
                                        className="h-8 w-8 p-0"
                                      >
                                        <X className="h-4 w-4" />
                                      </Button>
                                    </div>
                                  </div>
                                )
                              )}
                              <div className="flex justify-between items-center pt-2 border-t">
                                <span className="font-semibold">
                                  Enhancements Total:
                                </span>
                                <span className="text-lg font-bold text-primary">
                                  ${calculateEnhancementsTotal()}
                                </span>
                              </div>
                            </div>
                          )}

                          {/* Add Enhancement Dropdown */}
                          <div className="space-y-2">
                            <Label>Add Enhancement</Label>
                            {loadingEnhancements ? (
                              <div className="flex items-center gap-2 text-sm text-muted-foreground p-2">
                                <Loader2 className="h-4 w-4 animate-spin" />
                                Loading enhancements...
                              </div>
                            ) : enhancements && enhancements.length > 0 ? (
                              <Select
                                onValueChange={(value) => {
                                  const enhancement = enhancements.find(
                                    (e) => e.id === value
                                  );
                                  if (enhancement) {
                                    addEnhancement(enhancement);
                                  }
                                }}
                              >
                                <SelectTrigger>
                                  <SelectValue placeholder="Choose an enhancement to add" />
                                </SelectTrigger>
                                <SelectContent>
                                  {enhancements
                                    .filter(
                                      (e) => !selectedEnhancements.has(e.id)
                                    )
                                    .map((enhancement) => (
                                      <SelectItem
                                        key={enhancement.id}
                                        value={enhancement.id}
                                      >
                                        <div className="flex items-center justify-between gap-4">
                                          <span>{enhancement.name}</span>
                                          <span className="text-muted-foreground text-sm">
                                            ${enhancement.starting_price}
                                          </span>
                                        </div>
                                      </SelectItem>
                                    ))}
                                </SelectContent>
                              </Select>
                            ) : (
                              <p className="text-sm text-muted-foreground p-2">
                                No enhancements available
                              </p>
                            )}
                            <p className="text-xs text-muted-foreground">
                              Add optional extras to make your event even more
                              special
                            </p>
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
                            />
                          </div>
                        </div>

                        <Button
                          type="submit"
                          size="lg"
                          className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
                          disabled={isSubmitting}
                        >
                          {isSubmitting
                            ? "Submitting..."
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
                            We serve the greater metro area and surrounding
                            regions
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
                            All packages can be customized to fit your vision
                            and budget
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gradient-to-br from-primary/10 to-accent/10 border-primary/20">
                    <CardContent className="p-6 space-y-3">
                      <h3 className="font-semibold text-foreground">
                        Need Help?
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        Have questions about our services or packages? We're
                        here to help!
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
        </>
      ) : null}
      <AnonymousChat />
    </div>
  );
}
