"use client"

import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { useSearchParams } from "next/navigation"
import { AnonymousChat } from "@/components/anonymous-chat"

const themes = [
  {
    id: "garden-romance",
    title: "Garden Romance",
    category: "engagement",
    image: "/elegant-garden-wedding-decor-with-flowers-and-soft.jpg",
    colors: ["Blush", "Cream", "Gold"],
    description: "Elegant garden-inspired décor with soft florals and romantic touches",
  },
  {
    id: "whimsical-clouds",
    title: "Whimsical Clouds",
    category: "baby-shower",
    image: "/soft-cloud-themed-baby-shower-with-pastel-balloons.jpg",
    colors: ["Sky Blue", "White", "Pink"],
    description: "Dreamy cloud theme perfect for welcoming your little one",
  },
  {
    id: "golden-celebration",
    title: "Golden Celebration",
    category: "birthday",
    image: "/elegant-gold-and-cream-birthday-party-decor.jpg",
    colors: ["Gold", "Cream", "Blush"],
    description: "Luxurious gold accents for a memorable birthday celebration",
  },
  {
    id: "elegant-affair",
    title: "Elegant Affair",
    category: "engagement",
    image: "/elegant-event-decor-setup-with-flowers-and-soft-li.jpg",
    colors: ["Cream", "Gold", "White"],
    description: "Sophisticated and timeless décor for your special moment",
  },
  {
    id: "pastel-dreams",
    title: "Pastel Dreams",
    category: "baby-shower",
    image: "/soft-cloud-themed-baby-shower-with-pastel-balloons.jpg",
    colors: ["Pink", "Lavender", "Mint"],
    description: "Soft pastel palette creating a sweet and gentle atmosphere",
  },
  {
    id: "vintage-glam",
    title: "Vintage Glam",
    category: "birthday",
    image: "/elegant-gold-and-cream-birthday-party-decor.jpg",
    colors: ["Rose Gold", "Ivory", "Champagne"],
    description: "Classic vintage style with modern glamorous touches",
  },
]

const categories = [
  { value: "all", label: "All Events" },
  { value: "baby-shower", label: "Baby Showers" },
  { value: "birthday", label: "Birthdays" },
  { value: "engagement", label: "Engagements" },
]

export default function GalleryPage() {
  const searchParams = useSearchParams()
  const typeParam = searchParams.get("type")
  const [selectedCategory, setSelectedCategory] = useState(typeParam || "all")

  useEffect(() => {
    if (typeParam) {
      setSelectedCategory(typeParam)
    }
  }, [typeParam])

  const filteredThemes =
    selectedCategory === "all" ? themes : themes.filter((theme) => theme.category === selectedCategory)

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
              Explore our collection of stunning event themes and find the perfect style for your celebration
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
                variant={selectedCategory === category.value ? "default" : "outline"}
                onClick={() => setSelectedCategory(category.value)}
                className={selectedCategory === category.value ? "bg-primary text-primary-foreground" : ""}
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
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredThemes.map((theme, index) => (
              <motion.div
                key={theme.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Link href={`/gallery/${theme.id}`}>
                  <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 h-full">
                    <div className="relative overflow-hidden">
                      <img
                        src={theme.image || "/placeholder.svg"}
                        alt={theme.title}
                        className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute top-4 right-4 bg-primary/90 text-primary-foreground px-3 py-1 rounded-full text-sm capitalize">
                        {theme.category.replace("-", " ")}
                      </div>
                    </div>
                    <CardContent className="p-6 space-y-3">
                      <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                        {theme.title}
                      </h3>
                      <p className="text-muted-foreground text-sm leading-relaxed">{theme.description}</p>
                      <div className="flex gap-2 flex-wrap">
                        {theme.colors.map((color) => (
                          <span key={color} className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full">
                            {color}
                          </span>
                        ))}
                      </div>
                      <Button variant="link" className="p-0 h-auto text-primary">
                        View Details →
                      </Button>
                    </CardContent>
                  </Card>
                </Link>
              </motion.div>
            ))}
          </div>

          {filteredThemes.length === 0 && (
            <div className="text-center py-12">
              <p className="text-muted-foreground text-lg">No themes found in this category.</p>
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
              Let's create a custom theme that perfectly matches your vision and celebration style.
            </p>
            <Button asChild size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Link href="/booking">Book Your Event</Link>
            </Button>
          </motion.div>
        </div>
      </section>

      <Footer />

      <AnonymousChat />
    </div>
  )
}
