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
import { Loader2, Sparkles, Heart, Star, TrendingUp } from "lucide-react";
import { useGalleryItems } from "@/hooks/use-api-queries";

const categories = [
  { value: "all", label: "All Themes", icon: Sparkles },
  { value: "Baby Showers", label: "Baby Showers", icon: Heart },
  { value: "Birthdays", label: "Birthdays", icon: Star },
  { value: "Engagements", label: "Engagements", icon: Heart },
  { value: "Weddings", label: "Weddings", icon: Heart },
  { value: "Corporate", label: "Corporate Events", icon: TrendingUp },
];

export default function ThemesPage() {
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

  const themes = data?.items || [];
  const total = data?.total || 0;

  // Show error toast if fetch fails
  useEffect(() => {
    if (error) {
      toast({
        title: "Failed to Load Themes",
        description:
          (error as Error).message || "Could not load theme information",
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
            <div className="inline-flex items-center justify-center mb-4">
              <Sparkles className="h-12 w-12 text-primary" />
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-[family-name:var(--font-display)] text-balance">
              Event Themes
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Discover stunning themes for your celebration. From elegant and
              sophisticated to fun and whimsical, find the perfect style that
              brings your vision to life.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filter Section */}
      <section className="py-8 border-b border-border bg-card sticky top-0 z-40 backdrop-blur-sm bg-card/95">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap gap-3 justify-center">
            {categories.map((category) => {
              const Icon = category.icon;
              return (
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
                  <Icon className="h-4 w-4 mr-2" />
                  {category.label}
                </Button>
              );
            })}
          </div>

          {!isLoading && (
            <div className="text-center mt-4">
              <p className="text-sm text-muted-foreground">
                Showing {themes.length}{" "}
                {themes.length === 1 ? "theme" : "themes"}
                {selectedCategory !== "all" && ` in ${selectedCategory}`}
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Themes Grid */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : themes.length === 0 ? (
            <div className="text-center py-20">
              <Sparkles className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <p className="text-lg text-muted-foreground mb-2">
                No themes found in this category
              </p>
              <p className="text-sm text-muted-foreground mb-6">
                Try selecting a different category or check back soon for new
                themes
              </p>
              <Button
                onClick={() => setSelectedCategory("all")}
                variant="outline"
              >
                View All Themes
              </Button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {themes.map((theme, index) => (
                <motion.div
                  key={theme.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 h-full">
                    <div className="relative overflow-hidden aspect-[4/3]">
                      <img
                        src={theme.thumbnail_url || theme.image_url}
                        alt={theme.title}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/0 to-black/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                      {/* Category Badge */}
                      <div className="absolute top-4 right-4 bg-primary/90 text-primary-foreground px-3 py-1 rounded-full text-sm capitalize backdrop-blur-sm">
                        {theme.category}
                      </div>

                      {/* Featured Badge */}
                      {theme.is_featured && (
                        <div className="absolute top-4 left-4 bg-accent/90 text-accent-foreground px-3 py-1 rounded-full text-sm font-medium backdrop-blur-sm flex items-center gap-1">
                          <Star className="h-3 w-3 fill-current" />
                          Featured
                        </div>
                      )}

                      {/* Quick View on Hover */}
                      <div className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <Button
                          asChild
                          size="sm"
                          className="w-full bg-white/90 text-foreground hover:bg-white"
                        >
                          <Link href={`/booking?theme=${theme.id}`}>
                            Book This Theme
                          </Link>
                        </Button>
                      </div>
                    </div>

                    <CardContent className="p-6 space-y-3">
                      <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors line-clamp-1">
                        {theme.title}
                      </h3>

                      {theme.description && (
                        <p className="text-muted-foreground text-sm leading-relaxed line-clamp-2">
                          {theme.description}
                        </p>
                      )}

                      {theme.tags && theme.tags.length > 0 && (
                        <div className="flex gap-2 flex-wrap pt-2">
                          {theme.tags.slice(0, 3).map((tag) => (
                            <span
                              key={tag}
                              className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full capitalize"
                            >
                              {tag}
                            </span>
                          ))}
                          {theme.tags.length > 3 && (
                            <span className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full">
                              +{theme.tags.length - 3} more
                            </span>
                          )}
                        </div>
                      )}

                      <div className="pt-3">
                        <Button
                          asChild
                          variant="outline"
                          className="w-full"
                          size="sm"
                        >
                          <Link href={`/gallery/${theme.id}`}>
                            View Details
                          </Link>
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Info Section */}
      <section className="py-16 lg:py-24 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">
                Customizable Themes
              </h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Every theme can be customized to match your specific color
                palette, style preferences, and event requirements.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-center"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <Heart className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Made with Love</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Each theme is carefully curated and designed to create
                unforgettable moments for your special celebration.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-center"
            >
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4">
                <Star className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Expert Design</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Professional event designers craft each theme with attention to
                detail, color harmony, and visual impact.
              </p>
            </motion.div>
          </div>
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
              Ready to bring your vision to life?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Choose a theme and let's create a custom décor package that
              perfectly matches your celebration style and budget.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                asChild
                size="lg"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Link href="/booking">Book Your Event</Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/packages">View Packages</Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      <Footer />
      <AnonymousChat />
    </div>
  );
}
