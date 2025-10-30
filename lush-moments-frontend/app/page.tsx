"use client";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { AnonymousChat } from "@/components/anonymous-chat";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { Sparkles, Heart, Gift, Star, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import {
  useFeaturedThemes,
  useFeaturedTestimonials,
} from "@/hooks/use-api-queries";
import { useEffect } from "react";
import { useToast } from "@/hooks/use-toast";

const eventTypes = [
  {
    title: "Baby Showers",
    description: "Celebrate new beginnings with soft, dreamy décor",
    icon: Heart,
    color: "bg-primary/10 text-primary",
    href: "/gallery?type=Baby Showers",
  },
  {
    title: "Birthdays",
    description: "Make every year memorable with vibrant celebrations",
    icon: Gift,
    color: "bg-accent/10 text-accent-foreground",
    href: "/gallery?type=Birthdays",
  },
  {
    title: "Engagements",
    description: "Romance and elegance for your special moment",
    icon: Sparkles,
    color: "bg-primary/10 text-primary",
    href: "/gallery?type=Engagements",
  },
];

export default function HomePage() {
  const { toast } = useToast();

  // Fetch featured themes from API - cached for 24 hours (limited to 3)
  const {
    data: featuredData,
    isLoading: loadingThemes,
    error: themesError,
  } = useFeaturedThemes();
  const featuredThemes = featuredData?.items || [];

  // Fetch featured testimonials from API - cached for 24 hours (limited to 3)
  const {
    data: testimonialsData,
    isLoading: loadingTestimonials,
    error: testimonialsError,
  } = useFeaturedTestimonials();
  const testimonials = testimonialsData?.items || [];

  // Show error toast if fetch fails
  useEffect(() => {
    if (themesError) {
      toast({
        title: "Failed to Load Featured Themes",
        description:
          (themesError as Error).message || "Could not load featured themes",
        variant: "destructive",
      });
    }
    if (testimonialsError) {
      toast({
        title: "Failed to Load Testimonials",
        description:
          (testimonialsError as Error).message || "Could not load testimonials",
        variant: "destructive",
      });
    }
  }, [themesError, testimonialsError, toast]);

  return (
    <div className="min-h-screen">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/5 via-background to-accent/5">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-[family-name:var(--font-display)] text-balance leading-tight">
                Décor that makes every celebration{" "}
                <span className="text-primary font-bold">unforgettable</span>
              </h1>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Transform your special moments with elegant, personalized event
                décor that brings your vision to life.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  asChild
                  size="lg"
                  className="bg-primary text-primary-foreground hover:bg-primary/90"
                >
                  <Link href="/booking">Book Your Event</Link>
                </Button>
                <Button asChild size="lg" variant="outline">
                  <Link href="/gallery">View Gallery</Link>
                </Button>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <img
                src="/elegant-event-decor-setup-with-flowers-and-soft-li.jpg"
                alt="Elegant event décor"
                className="rounded-2xl shadow-2xl w-full"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Quick Select Event Types */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl sm:text-4xl font-[family-name:var(--font-display)] text-balance mb-4">
              What are you celebrating?
            </h2>
            <p className="text-muted-foreground text-lg">
              Choose your event type to explore our curated themes
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {eventTypes.map((event, index) => {
              const Icon = event.icon;
              return (
                <motion.div
                  key={event.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Link href={event.href}>
                    <Card className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer border-2 hover:border-primary/50">
                      <CardContent className="p-8 text-center space-y-4">
                        <div
                          className={`inline-flex p-4 rounded-full ${event.color}`}
                        >
                          <Icon className="h-8 w-8" />
                        </div>
                        <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                          {event.title}
                        </h3>
                        <p className="text-muted-foreground leading-relaxed">
                          {event.description}
                        </p>
                      </CardContent>
                    </Card>
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Featured Themes */}
      <section className="py-16 lg:py-24 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl sm:text-4xl font-[family-name:var(--font-display)] text-balance mb-4">
              Featured Themes
            </h2>
            <p className="text-muted-foreground text-lg">
              Discover our most popular décor collections
            </p>
          </motion.div>

          {loadingThemes ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : featuredThemes.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-muted-foreground">
                No featured themes available at the moment.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-3 gap-8">
              {featuredThemes.map((theme, index) => (
                <motion.div
                  key={theme.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Link href={`/gallery/${theme.id}`}>
                    <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer">
                      <div className="relative overflow-hidden">
                        <img
                          src={theme.thumbnail_url || theme.image_url}
                          alt={theme.title}
                          className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                        <div className="absolute top-4 right-4 bg-primary/90 text-primary-foreground px-3 py-1 rounded-full text-sm capitalize">
                          {theme.category}
                        </div>
                        <div className="absolute top-4 left-4 bg-accent/90 text-accent-foreground px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                          <Star className="h-3 w-3 fill-current" />
                          Featured
                        </div>
                      </div>
                      <CardContent className="p-6 space-y-3">
                        <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                          {theme.title}
                        </h3>
                        {theme.description && (
                          <p className="text-sm text-muted-foreground line-clamp-2">
                            {theme.description}
                          </p>
                        )}
                        {theme.tags && theme.tags.length > 0 && (
                          <div className="flex gap-2 flex-wrap">
                            {theme.tags.slice(0, 3).map((tag) => (
                              <span
                                key={tag}
                                className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full capitalize"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                        <Button
                          variant="link"
                          className="p-0 h-auto text-primary"
                        >
                          View Details →
                        </Button>
                      </CardContent>
                    </Card>
                  </Link>
                </motion.div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Button asChild size="lg" variant="outline">
              <Link href="/themes">View All Themes</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl sm:text-4xl font-[family-name:var(--font-display)] text-balance mb-4">
              What our clients say
            </h2>
            <p className="text-muted-foreground text-lg">
              Real stories from real celebrations
            </p>
          </motion.div>

          {loadingTestimonials ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : testimonials.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-muted-foreground">
                No testimonials available at the moment.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-3 gap-8">
              {testimonials.map((testimonial, index) => (
                <motion.div
                  key={testimonial.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card className="h-full">
                    <CardContent className="p-6 space-y-4">
                      <div className="flex gap-1">
                        {Array.from({ length: testimonial.rating }).map(
                          (_, i) => (
                            <Star
                              key={i}
                              className="h-5 w-5 fill-accent text-accent"
                            />
                          )
                        )}
                      </div>
                      <p className="text-muted-foreground leading-relaxed italic">
                        "{testimonial.message}"
                      </p>
                      <div className="pt-4 border-t border-border">
                        <p className="font-semibold text-foreground">
                          {testimonial.name}
                        </p>
                        {testimonial.event_type && (
                          <p className="text-sm text-muted-foreground">
                            {testimonial.event_type}
                          </p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
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
              Ready to create your perfect celebration?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Let's bring your vision to life with personalized décor that makes
              your event truly unforgettable.
            </p>
            <Button
              asChild
              size="lg"
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              <Link href="/booking">Start Planning Today</Link>
            </Button>
          </motion.div>
        </div>
      </section>

      <Footer />
      <AnonymousChat />
    </div>
  );
}
