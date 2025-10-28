"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"
import { motion } from "framer-motion"
import { ArrowLeft, Palette, Sparkles, Heart } from "lucide-react"

type Theme = {
  title: string
  category: string
  images: string[]
  colors: string[]
  description: string
  features: string[]
  moodboard?: string
}

export function ThemeDetail({ theme, id }: { theme: Theme | undefined; id: string }) {
  if (!theme) {
    return (
      <div className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-3xl font-[family-name:var(--font-display)] mb-4">Theme Not Found</h1>
        <Button asChild>
          <Link href="/gallery">Back to Gallery</Link>
        </Button>
      </div>
    )
  }

  return (
    <>
      {/* Back Button */}
      <section className="py-6 border-b border-border">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <Button variant="ghost" asChild>
            <Link href="/gallery">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Gallery
            </Link>
          </Button>
        </div>
      </section>

      {/* Hero Section */}
      <section className="py-16 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-start">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-6"
            >
              <div className="inline-block bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium">
                {theme.category}
              </div>
              <h1 className="text-4xl sm:text-5xl font-[family-name:var(--font-display)] text-balance">
                {theme.title}
              </h1>
              <p className="text-lg text-muted-foreground leading-relaxed">{theme.description}</p>

              {/* Color Palette */}
              <Card>
                <CardContent className="p-6 space-y-4">
                  <div className="flex items-center gap-2 text-foreground">
                    <Palette className="h-5 w-5 text-primary" />
                    <h3 className="font-semibold">Color Palette</h3>
                  </div>
                  <div className="flex gap-2 flex-wrap">
                    {theme.colors.map((color) => (
                      <span key={color} className="bg-muted text-muted-foreground px-3 py-1.5 rounded-full text-sm">
                        {color}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Features */}
              <Card>
                <CardContent className="p-6 space-y-4">
                  <div className="flex items-center gap-2 text-foreground">
                    <Sparkles className="h-5 w-5 text-primary" />
                    <h3 className="font-semibold">What's Included</h3>
                  </div>
                  <ul className="space-y-2">
                    {theme.features.map((feature, index) => (
                      <li key={index} className="flex items-start gap-2 text-muted-foreground">
                        <Heart className="h-4 w-4 text-primary mt-1 flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              <Button asChild size="lg" className="w-full bg-primary text-primary-foreground hover:bg-primary/90">
                <Link href="/booking">Book This Theme</Link>
              </Button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="space-y-6"
            >
              {theme.images.map((image, index) => (
                <img
                  key={index}
                  src={image || "/placeholder.svg"}
                  alt={`${theme.title} - Image ${index + 1}`}
                  className="rounded-2xl shadow-lg w-full"
                />
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Related Themes */}
      <section className="py-16 lg:py-24 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-[family-name:var(--font-display)] text-center mb-12">Explore More Themes</h2>
          <div className="text-center">
            <Button asChild size="lg" variant="outline">
              <Link href="/gallery">View All Themes</Link>
            </Button>
          </div>
        </div>
      </section>
    </>
  )
}
