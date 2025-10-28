"use client"

import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { AnonymousChat } from "@/components/anonymous-chat"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { Sparkles, Heart, Gift, Star } from "lucide-react"
import { motion } from "framer-motion"

const eventTypes = [
  {
    title: "Baby Showers",
    description: "Celebrate new beginnings with soft, dreamy décor",
    icon: Heart,
    color: "bg-primary/10 text-primary",
    href: "/gallery?type=baby-shower",
  },
  {
    title: "Birthdays",
    description: "Make every year memorable with vibrant celebrations",
    icon: Gift,
    color: "bg-accent/10 text-accent-foreground",
    href: "/gallery?type=birthday",
  },
  {
    title: "Engagements",
    description: "Romance and elegance for your special moment",
    icon: Sparkles,
    color: "bg-primary/10 text-primary",
    href: "/gallery?type=engagement",
  },
]

const featuredThemes = [
  {
    title: "Garden Romance",
    category: "Engagement",
    image: "/elegant-garden-wedding-decor-with-flowers-and-soft.jpg",
    colors: ["Blush", "Cream", "Gold"],
  },
  {
    title: "Whimsical Clouds",
    category: "Baby Shower",
    image: "/soft-cloud-themed-baby-shower-with-pastel-balloons.jpg",
    colors: ["Sky Blue", "White", "Pink"],
  },
  {
    title: "Golden Celebration",
    category: "Birthday",
    image: "/elegant-gold-and-cream-birthday-party-decor.jpg",
    colors: ["Gold", "Cream", "Blush"],
  },
]

const testimonials = [
  {
    name: "Sarah Johnson",
    event: "Baby Shower",
    text: "Lush Moments transformed my baby shower into a magical experience. Every detail was perfect!",
    rating: 5,
  },
  {
    name: "Michael Chen",
    event: "Engagement Party",
    text: "The team brought our vision to life beautifully. Our guests are still talking about the décor!",
    rating: 5,
  },
  {
    name: "Emily Rodriguez",
    event: "Birthday Party",
    text: "Professional, creative, and absolutely stunning work. Highly recommend for any celebration!",
    rating: 5,
  },
]

export default function HomePage() {
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
                Décor that makes every celebration <span className="text-primary font-bold">unforgettable</span>
              </h1>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Transform your special moments with elegant, personalized event décor that brings your vision to life.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button asChild size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
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
            <p className="text-muted-foreground text-lg">Choose your event type to explore our curated themes</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {eventTypes.map((event, index) => {
              const Icon = event.icon
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
                        <div className={`inline-flex p-4 rounded-full ${event.color}`}>
                          <Icon className="h-8 w-8" />
                        </div>
                        <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                          {event.title}
                        </h3>
                        <p className="text-muted-foreground leading-relaxed">{event.description}</p>
                      </CardContent>
                    </Card>
                  </Link>
                </motion.div>
              )
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
            <p className="text-muted-foreground text-lg">Discover our most popular décor collections</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {featuredThemes.map((theme, index) => (
              <motion.div
                key={theme.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300">
                  <div className="relative overflow-hidden">
                    <img
                      src={theme.image || "/placeholder.svg"}
                      alt={theme.title}
                      className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div className="absolute top-4 right-4 bg-primary/90 text-primary-foreground px-3 py-1 rounded-full text-sm">
                      {theme.category}
                    </div>
                  </div>
                  <CardContent className="p-6 space-y-3">
                    <h3 className="text-xl font-semibold text-foreground">{theme.title}</h3>
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
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button asChild size="lg" variant="outline">
              <Link href="/gallery">View All Themes</Link>
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
            <p className="text-muted-foreground text-lg">Real stories from real celebrations</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="h-full">
                  <CardContent className="p-6 space-y-4">
                    <div className="flex gap-1">
                      {Array.from({ length: testimonial.rating }).map((_, i) => (
                        <Star key={i} className="h-5 w-5 fill-accent text-accent" />
                      ))}
                    </div>
                    <p className="text-muted-foreground leading-relaxed italic">"{testimonial.text}"</p>
                    <div className="pt-4 border-t border-border">
                      <p className="font-semibold text-foreground">{testimonial.name}</p>
                      <p className="text-sm text-muted-foreground">{testimonial.event}</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
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
              Ready to create your perfect celebration?
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Let's bring your vision to life with personalized décor that makes your event truly unforgettable.
            </p>
            <Button asChild size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
              <Link href="/booking">Start Planning Today</Link>
            </Button>
          </motion.div>
        </div>
      </section>

      <Footer />
      <AnonymousChat />
    </div>
  )
}
