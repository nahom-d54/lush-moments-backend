"use client";

import { Navigation } from "@/components/navigation";
import { Footer } from "@/components/footer";
import { AnonymousChat } from "@/components/anonymous-chat";
import { motion } from "framer-motion";
import { Loader2, Search } from "lucide-react";
import { useFAQs, useFAQCategories } from "@/hooks/use-api-queries";
import { useState, useMemo } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function FAQPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");

  const { data: faqs = [], isLoading: faqsLoading } = useFAQs(
    selectedCategory === "all" ? undefined : selectedCategory
  );
  const { data: categoriesData, isLoading: categoriesLoading } =
    useFAQCategories();

  const categories = categoriesData?.categories || [];

  // Filter FAQs based on search query
  const filteredFaqs = useMemo(() => {
    if (!searchQuery.trim()) return faqs;

    const query = searchQuery.toLowerCase();
    return faqs.filter(
      (faq) =>
        faq.question.toLowerCase().includes(query) ||
        faq.answer.toLowerCase().includes(query)
    );
  }, [faqs, searchQuery]);

  // Group FAQs by category
  const groupedFaqs = useMemo(() => {
    const groups: Record<string, typeof faqs> = {};
    filteredFaqs.forEach((faq) => {
      if (!groups[faq.category]) {
        groups[faq.category] = [];
      }
      groups[faq.category].push(faq);
    });
    return groups;
  }, [filteredFaqs]);

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
              Frequently Asked Questions
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Find answers to common questions about our event decoration
              services, booking process, and more.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Search and Filter Section */}
      <section className="py-12 border-b">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto space-y-6">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                placeholder="Search FAQs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Category Filters */}
            {categoriesLoading ? (
              <div className="flex justify-center">
                <Loader2 className="h-6 w-6 animate-spin text-primary" />
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                <Button
                  variant={selectedCategory === "all" ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory("all")}
                >
                  All
                </Button>
                {categories.map((category) => (
                  <Button
                    key={category}
                    variant={
                      selectedCategory === category ? "default" : "outline"
                    }
                    size="sm"
                    onClick={() => setSelectedCategory(category)}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </Button>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* FAQs Section */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto">
            {faqsLoading ? (
              <div className="flex justify-center items-center py-20">
                <Loader2 className="h-12 w-12 animate-spin text-primary" />
              </div>
            ) : filteredFaqs.length === 0 ? (
              <div className="text-center py-20">
                <p className="text-lg text-muted-foreground">
                  {searchQuery
                    ? "No FAQs found matching your search."
                    : "No FAQs available at the moment."}
                </p>
              </div>
            ) : selectedCategory === "all" ? (
              // Show grouped by category
              <div className="space-y-12">
                {Object.entries(groupedFaqs).map(([category, categoryFaqs]) => (
                  <motion.div
                    key={category}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                  >
                    <div className="mb-6">
                      <Badge variant="secondary" className="text-sm px-3 py-1">
                        {category.charAt(0).toUpperCase() + category.slice(1)}
                      </Badge>
                    </div>
                    <Accordion type="single" collapsible className="space-y-4">
                      {categoryFaqs.map((faq, index) => (
                        <motion.div
                          key={faq.id}
                          initial={{ opacity: 0, y: 20 }}
                          whileInView={{ opacity: 1, y: 0 }}
                          viewport={{ once: true }}
                          transition={{ duration: 0.6, delay: index * 0.05 }}
                        >
                          <AccordionItem
                            value={faq.id}
                            className="border rounded-lg px-6 bg-card hover:shadow-md transition-shadow"
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
                  </motion.div>
                ))}
              </div>
            ) : (
              // Show single category
              <Accordion type="single" collapsible className="space-y-4">
                {filteredFaqs.map((faq, index) => (
                  <motion.div
                    key={faq.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.05 }}
                  >
                    <AccordionItem
                      value={faq.id}
                      className="border rounded-lg px-6 bg-card hover:shadow-md transition-shadow"
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
              Still have questions?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              We're here to help! Contact us directly or use our chat feature to
              get personalized assistance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                asChild
                size="lg"
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                <a href="/contact">Contact Us</a>
              </Button>
              <Button asChild size="lg" variant="outline">
                <a href="/booking">Get a Quote</a>
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
