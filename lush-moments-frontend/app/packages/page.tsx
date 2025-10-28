"use client"

import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import Link from "next/link"
import { motion } from "framer-motion"
import { Check, Sparkles, Crown, Star } from "lucide-react"
import { AnonymousChat } from "@/components/anonymous-chat"

const packages = [
  {
    name: "Essential",
    icon: Star,
    price: "Starting at $500",
    description: "Perfect for intimate gatherings and smaller celebrations",
    features: [
      "Basic décor setup for up to 30 guests",
      "Color-coordinated balloon arrangements",
      "Table centerpieces (3-5 tables)",
      "Welcome signage",
      "2 hours of setup time",
      "Basic cleanup service",
    ],
    popular: false,
    color: "text-primary",
  },
  {
    name: "Deluxe",
    icon: Sparkles,
    price: "Starting at $1,200",
    description: "Our most popular package for memorable celebrations",
    features: [
      "Complete décor setup for up to 75 guests",
      "Premium balloon installations",
      "Elegant table centerpieces (up to 10 tables)",
      "Custom backdrop for photos",
      "Welcome signage and directional signs",
      "Themed dessert table styling",
      "4 hours of setup time",
      "Full cleanup service",
      "Consultation and design planning",
    ],
    popular: true,
    color: "text-accent",
  },
  {
    name: "Signature",
    icon: Crown,
    price: "Starting at $2,500",
    description: "Luxury décor for unforgettable celebrations",
    features: [
      "Premium décor setup for 100+ guests",
      "Elaborate balloon installations and arches",
      "Luxury floral arrangements",
      "Custom centerpieces (unlimited tables)",
      "Professional photo backdrop with props",
      "Complete dessert table design",
      "Lounge area styling",
      "Custom signage package",
      "Ambient lighting design",
      "6 hours of setup time",
      "Full event coordination",
      "Complete cleanup service",
      "Multiple design consultations",
    ],
    popular: false,
    color: "text-secondary",
  },
]

const addOns = [
  {
    title: "Floral Arrangements",
    description: "Fresh or silk floral centerpieces and accents",
    price: "From $150",
  },
  {
    title: "Photo Booth Setup",
    description: "Custom backdrop with props and signage",
    price: "From $300",
  },
  {
    title: "Lighting Design",
    description: "Ambient uplighting and string lights",
    price: "From $200",
  },
  {
    title: "Dessert Table Styling",
    description: "Complete dessert display with décor",
    price: "From $250",
  },
  {
    title: "Lounge Area",
    description: "Comfortable seating area with décor",
    price: "From $400",
  },
  {
    title: "Custom Signage",
    description: "Personalized welcome and directional signs",
    price: "From $100",
  },
]

export default function PackagesPage() {
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
              Choose the perfect package for your celebration. All packages are customizable to match your vision and
              budget.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Packages Grid */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            {packages.map((pkg, index) => {
              const Icon = pkg.icon
              return (
                <motion.div
                  key={pkg.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="relative"
                >
                  {pkg.popular && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm font-medium z-10">
                      Most Popular
                    </div>
                  )}
                  <Card
                    className={`h-full ${pkg.popular ? "border-primary border-2 shadow-lg" : ""} hover:shadow-xl transition-shadow`}
                  >
                    <CardHeader className="text-center space-y-4 pb-8">
                      <div className={`inline-flex justify-center`}>
                        <div className="p-4 bg-primary/10 rounded-full">
                          <Icon className={`h-8 w-8 ${pkg.color}`} />
                        </div>
                      </div>
                      <div>
                        <h3 className="text-2xl font-[family-name:var(--font-display)] mb-2">{pkg.name}</h3>
                        <p className="text-3xl font-bold text-foreground mb-2">{pkg.price}</p>
                        <p className="text-sm text-muted-foreground">{pkg.description}</p>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <ul className="space-y-3">
                        {pkg.features.map((feature, i) => (
                          <li key={i} className="flex items-start gap-3">
                            <Check className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                            <span className="text-sm text-muted-foreground">{feature}</span>
                          </li>
                        ))}
                      </ul>
                      <Button
                        asChild
                        className={`w-full ${pkg.popular ? "bg-primary text-primary-foreground hover:bg-primary/90" : ""}`}
                        variant={pkg.popular ? "default" : "outline"}
                      >
                        <Link href="/booking">Get Quote</Link>
                      </Button>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Add-ons Section */}
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
            <p className="text-muted-foreground text-lg">Add these extras to make your celebration even more special</p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {addOns.map((addon, index) => (
              <motion.div
                key={addon.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardContent className="p-6 space-y-3">
                    <div className="flex items-start justify-between">
                      <h3 className="font-semibold text-foreground">{addon.title}</h3>
                      <span className="text-primary font-semibold text-sm">{addon.price}</span>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">{addon.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
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

          <div className="max-w-3xl mx-auto space-y-6">
            <Card>
              <CardContent className="p-6 space-y-2">
                <h3 className="font-semibold text-foreground">Can I customize a package?</h3>
                <p className="text-muted-foreground leading-relaxed">
                  All our packages are fully customizable. We'll work with you to create the perfect décor that matches
                  your vision and budget.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6 space-y-2">
                <h3 className="font-semibold text-foreground">How far in advance should I book?</h3>
                <p className="text-muted-foreground leading-relaxed">
                  We recommend booking at least 4-6 weeks in advance for best availability. However, we'll do our best
                  to accommodate last-minute requests.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6 space-y-2">
                <h3 className="font-semibold text-foreground">Do you provide setup and cleanup?</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Yes! All packages include professional setup and cleanup services. You can focus on enjoying your
                  celebration while we handle the details.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6 space-y-2">
                <h3 className="font-semibold text-foreground">What areas do you serve?</h3>
                <p className="text-muted-foreground leading-relaxed">
                  We serve the greater metropolitan area and surrounding regions. Contact us to confirm service
                  availability for your location.
                </p>
              </CardContent>
            </Card>
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
              Let's discuss your event and create a custom package that brings your vision to life.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90">
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
  )
}
