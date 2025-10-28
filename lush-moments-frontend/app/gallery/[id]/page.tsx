import { Navigation } from "@/components/navigation"
import { Footer } from "@/components/footer"
import { AnonymousChat } from "@/components/anonymous-chat"
import { ThemeDetail } from "@/components/theme-detail"

const themesData: Record<
  string,
  {
    title: string
    category: string
    images: string[]
    colors: string[]
    description: string
    features: string[]
    moodboard?: string
  }
> = {
  "garden-romance": {
    title: "Garden Romance",
    category: "Engagement",
    images: [
      "/elegant-garden-wedding-decor-with-flowers-and-soft.jpg",
      "/elegant-event-decor-setup-with-flowers-and-soft-li.jpg",
    ],
    colors: ["Blush Pink", "Cream", "Gold", "Sage Green"],
    description:
      "Create an enchanting garden atmosphere with soft florals, romantic lighting, and elegant touches. Perfect for engagements and intimate celebrations.",
    features: [
      "Fresh floral arrangements with roses and peonies",
      "Elegant table settings with gold accents",
      "Romantic string lighting and candles",
      "Custom signage and place cards",
      "Coordinated linens and chair covers",
    ],
  },
  "whimsical-clouds": {
    title: "Whimsical Clouds",
    category: "Baby Shower",
    images: ["/soft-cloud-themed-baby-shower-with-pastel-balloons.jpg"],
    colors: ["Sky Blue", "White", "Soft Pink", "Lavender"],
    description:
      "Float away on dreamy clouds with this whimsical baby shower theme. Soft pastels and cloud motifs create a magical atmosphere for welcoming your little one.",
    features: [
      "Cloud balloon installations",
      "Pastel color palette throughout",
      "Custom cloud backdrop for photos",
      "Themed dessert table styling",
      "Coordinated tableware and decorations",
    ],
  },
  "golden-celebration": {
    title: "Golden Celebration",
    category: "Birthday",
    images: ["/elegant-gold-and-cream-birthday-party-decor.jpg"],
    colors: ["Gold", "Cream", "Blush", "Champagne"],
    description:
      "Celebrate in style with luxurious gold accents and elegant cream tones. This sophisticated theme is perfect for milestone birthdays and special celebrations.",
    features: [
      "Gold balloon arrangements and garlands",
      "Elegant table centerpieces",
      "Custom birthday backdrop",
      "Coordinated dessert display",
      "Premium tableware and linens",
    ],
  },
  "elegant-affair": {
    title: "Elegant Affair",
    category: "Engagement",
    images: ["/elegant-event-decor-setup-with-flowers-and-soft-li.jpg"],
    colors: ["Cream", "Gold", "White", "Champagne"],
    description:
      "Timeless elegance meets modern sophistication in this refined theme. Perfect for engagements and upscale celebrations.",
    features: [
      "Sophisticated floral arrangements",
      "Premium table settings",
      "Ambient lighting design",
      "Custom welcome signage",
      "Coordinated color scheme throughout",
    ],
  },
  "pastel-dreams": {
    title: "Pastel Dreams",
    category: "Baby Shower",
    images: ["/soft-cloud-themed-baby-shower-with-pastel-balloons.jpg"],
    colors: ["Soft Pink", "Lavender", "Mint", "Peach"],
    description: "Sweet and gentle pastel hues create a dreamy atmosphere perfect for celebrating new beginnings.",
    features: [
      "Pastel balloon arrangements",
      "Soft floral accents",
      "Themed dessert table",
      "Custom baby shower signage",
      "Coordinated party favors",
    ],
  },
  "vintage-glam": {
    title: "Vintage Glam",
    category: "Birthday",
    images: ["/elegant-gold-and-cream-birthday-party-decor.jpg"],
    colors: ["Rose Gold", "Ivory", "Champagne", "Blush"],
    description:
      "Classic vintage charm with a modern glamorous twist. Perfect for sophisticated birthday celebrations.",
    features: [
      "Vintage-inspired centerpieces",
      "Rose gold accents throughout",
      "Elegant table settings",
      "Custom photo backdrop",
      "Premium party supplies",
    ],
  },
}

export default async function ThemeDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const theme = themesData[id]

  return (
    <div className="min-h-screen">
      <Navigation />
      <ThemeDetail theme={theme} id={id} />
      <Footer />
      <AnonymousChat />
    </div>
  )
}
