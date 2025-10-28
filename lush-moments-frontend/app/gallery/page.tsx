"use client";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useSearchParams } from "next/navigation";
import { AnonymousChat } from "@/components/anonymous-chat";
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from "lucide-react";
import { useGalleryItems } from "@/hooks/use-api-queries";

const categories = [
  { value: "all", label: "All Events" },
  { value: "Baby Showers", label: "Baby Showers" },
  { value: "Birthdays", label: "Birthdays" },
  { value: "Engagements", label: "Engagements" },
];

export default function GalleryPage() {
  const { toast } = useToast();
  const searchParams = useSearchParams();
  const typeParam = searchParams.get("type");
  const [selectedCategory, setSelectedCategory] = useState(typeParam || "all");

  useEffect(() => {
    if (typeParam) {
      setSelectedCategory(typeParam);
    }
  }, [typeParam]);

  // Use custom hook with TanStack Query - caches for 24 hours
  const { data, isLoading, error } = useGalleryItems(selectedCategory);

  const galleryItems = data?.items || [];
  const total = data?.total || 0;

  // Show error toast if fetch fails
  useEffect(() => {
    if (error) {
      toast({
        title: "Failed to Load Gallery",
        description: (error as Error).message || "Could not load gallery items",
        variant: "destructive",
      });
    }
  }, [error, toast]);

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
              Our Gallery
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Explore our collection of stunning event themes and find the
              perfect style for your celebration
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filter Section */}
      <section className="py-8 border-b border-border bg-card">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap gap-3 justify-center">
            {categories.map((category) => (
              <Button
                key={category.value}
                variant={
                  selectedCategory === category.value ? "default" : "outline"
                }
                onClick={() => setSelectedCategory(category.value)}
                className={
                  selectedCategory === category.value
                    ? "bg-primary text-primary-foreground"
                    : ""
                }
              >
                {category.label}
              </Button>
            ))}
          </div>
        </div>
      </section>

      {/* Gallery Grid */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : galleryItems.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-lg text-muted-foreground">
                No gallery items found in this category.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {galleryItems.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 h-full">
                    <div className="relative overflow-hidden">
                      <img
                        src={item.thumbnail_url || item.image_url}
                        alt={item.title}
                        className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute top-4 right-4 bg-primary/90 text-primary-foreground px-3 py-1 rounded-full text-sm capitalize">
                        {item.category}
                      </div>
                      {item.is_featured && (
                        <div className="absolute top-4 left-4 bg-accent/90 text-accent-foreground px-3 py-1 rounded-full text-sm font-medium">
                          Featured
                        </div>
                      )}
                    </div>
                    <CardContent className="p-6 space-y-3">
                      <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                        {item.title}
                      </h3>
                      {item.description && (
                        <p className="text-muted-foreground text-sm leading-relaxed line-clamp-2">
                          {item.description}
                        </p>
                      )}
                      {item.tags && item.tags.length > 0 && (
                        <div className="flex gap-2 flex-wrap">
                          {item.tags.slice(0, 4).map((tag) => (
                            <span
                              key={tag}
                              className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full"
                            >
                              {tag}
                            </span>
                          ))}
                          {item.tags.length > 4 && (
                            <span className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full">
                              +{item.tags.length - 4}
                            </span>
                          )}
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
              Love what you see?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Let's create a custom theme that perfectly matches your vision and
              celebration style.
            </p>
            <Button
              asChild
              size="lg"
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              <Link href="/booking">Book Your Event</Link>
            </Button>
          </motion.div>
        </div>
      </section>

      <Footer />

      <AnonymousChat />
    </div>
  );
}
