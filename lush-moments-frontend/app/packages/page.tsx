"use client";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import Link from "next/link";
import { motion } from "framer-motion";
import { Check, Sparkles, Crown, Star, Loader2 } from "lucide-react";
import { AnonymousChat } from "@/components/anonymous-chat";
import { useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { usePackages, useFAQs, useEnhancements } from "@/hooks/use-api-queries";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

// Icon mapping based on package title
const getPackageIcon = (title: string) => {
  const lowerTitle = title.toLowerCase();
  if (lowerTitle.includes("essential") || lowerTitle.includes("basic"))
    return Star;
  if (lowerTitle.includes("deluxe") || lowerTitle.includes("premium"))
    return Sparkles;
  if (lowerTitle.includes("signature") || lowerTitle.includes("luxury"))
    return Crown;
  return Star;
};

// Color mapping
const getPackageColor = (index: number) => {
  const colors = ["text-primary", "text-accent", "text-secondary"];
  return colors[index % colors.length];
};

export default function PackagesPage() {
  const { toast } = useToast();

  // Use TanStack Query hooks with caching
  const { data: packages = [], isLoading, error } = usePackages();
  const {
    data: enhancements = [],
    isLoading: enhancementsLoading,
    error: enhancementsError,
  } = useEnhancements();
  const {
    data: faqs = [],
    isLoading: faqsLoading,
    error: faqsError,
  } = useFAQs();

  // Show error toast if fetch fails
  useEffect(() => {
    if (error) {
      toast({
        title: "Failed to Load Packages",
        description:
          (error as Error).message || "Could not load package information",
        variant: "destructive",
      });
    }
    if (enhancementsError) {
      toast({
        title: "Failed to Load Enhancements",
        description:
          (enhancementsError as Error).message ||
          "Could not load enhancement information",
        variant: "destructive",
      });
    }
    if (faqsError) {
      toast({
        title: "Failed to Load FAQs",
        description:
          (faqsError as Error).message || "Could not load FAQ information",
        variant: "destructive",
      });
    }
  }, [error, enhancementsError, faqsError, toast]);

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
              Our Packages
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Choose the perfect package for your celebration. All packages are
              customizable to match your vision and budget.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Packages Grid */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <Loader2 className="h-12 w-12 animate-spin text-primary" />
            </div>
          ) : packages.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-lg text-muted-foreground">
                No packages available at the moment.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-3 gap-8">
              {packages.map((pkg, index) => {
                const Icon = getPackageIcon(pkg.title);
                const color = getPackageColor(index);
                return (
                  <motion.div
                    key={pkg.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    className="relative"
                  >
                    {pkg.is_popular && (
                      <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm font-medium z-10">
                        Most Popular
                      </div>
                    )}
                    <Card
                      className={`h-full ${
                        pkg.is_popular
                          ? "border-primary border-2 shadow-lg"
                          : ""
                      } hover:shadow-xl transition-shadow`}
                    >
                      <CardHeader className="text-center space-y-4 pb-8">
                        <div className={`inline-flex justify-center`}>
                          <div className="p-4 bg-primary/10 rounded-full">
                            <Icon className={`h-8 w-8 ${color}`} />
                          </div>
                        </div>
                        <div>
                          <h3 className="text-2xl font-[family-name:var(--font-display)] mb-2">
                            {pkg.title}
                          </h3>
                          <p className="text-3xl font-bold text-foreground mb-2">
                            ${pkg.price.toLocaleString()}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {pkg.description}
                          </p>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-6">
                        <ul className="space-y-3">
                          {pkg.items.map((item) => (
                            <li
                              key={item.id}
                              className="flex items-start gap-3"
                            >
                              <Check className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                              <span className="text-sm text-muted-foreground">
                                {item.item_text}
                              </span>
                            </li>
                          ))}
                        </ul>
                        <Button
                          asChild
                          className={`w-full ${
                            pkg.is_popular
                              ? "bg-primary text-primary-foreground hover:bg-primary/90"
                              : ""
                          }`}
                          variant={pkg.is_popular ? "default" : "outline"}
                        >
                          <Link href={`/booking?package=${pkg.id}`}>
                            Get Quote
                          </Link>
                        </Button>
                      </CardContent>
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          )}
        </div>
      </section>

      {/* Add-ons Section - Dynamic from API */}
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
              Enhance Your Package
            </h2>
            <p className="text-muted-foreground text-lg">
              Add these extras to make your celebration even more special
            </p>
          </motion.div>

          {enhancementsLoading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : enhancements.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">
                No enhancements available at the moment.
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {enhancements.map((enhancement, index) => (
                <motion.div
                  key={enhancement.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.05 }}
                >
                  <Card className="h-full hover:shadow-lg transition-shadow">
                    <CardContent className="p-6 space-y-3">
                      <div className="flex items-start justify-between">
                        <h3 className="font-semibold text-foreground">
                          {enhancement.name}
                        </h3>
                        <span className="text-primary font-semibold text-sm whitespace-nowrap ml-2">
                          From ${enhancement.starting_price}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {enhancement.description}
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* FAQ Section - Dynamic from API */}
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
              Frequently Asked Questions
            </h2>
          </motion.div>

          <div className="max-w-3xl mx-auto">
            {faqsLoading ? (
              <div className="flex justify-center items-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : faqs.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">
                  No FAQs available at the moment.
                </p>
              </div>
            ) : (
              <Accordion type="single" collapsible className="space-y-4">
                {faqs.map((faq, index) => (
                  <motion.div
                    key={faq.id}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: index * 0.05 }}
                  >
                    <AccordionItem
                      value={faq.id}
                      className="border rounded-lg px-6 bg-card"
                    >
                      <AccordionTrigger className="hover:no-underline py-4">
                        <span className="font-semibold text-foreground text-left">
                          {faq.question}
                        </span>
                      </AccordionTrigger>
                      <AccordionContent className="text-muted-foreground leading-relaxed pb-4">
                        {faq.answer}
                      </AccordionContent>
                    </AccordionItem>
                  </motion.div>
                ))}
              </Accordion>
            )}
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
              Ready to get started?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Let's discuss your event and create a custom package that brings
              your vision to life.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                asChild
                size="lg"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <Link href="/booking">Get a Quote</Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/contact">Contact Us</Link>
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
