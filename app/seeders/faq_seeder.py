"""
FAQ Seeder

Seeds frequently asked questions.
"""

from sqlalchemy import select

from app.models import FAQ

from .base import BaseSeeder
from .registry import registry


class FAQSeeder(BaseSeeder):
    """Seed FAQ data"""

    name = "faqs"
    description = "Create frequently asked questions"
    dependencies = []

    async def should_run(self) -> bool:
        """Check if FAQs already exist"""
        result = await self.db.execute(select(FAQ).limit(1))
        return result.first() is None

    async def run(self) -> None:
        """Create FAQs"""
        faqs_data = [
            {
                "question": "How do I book your services?",
                "answer": "You can book our services through our website's booking form, call us directly, or send us an email. We'll schedule a free consultation to discuss your event details.",
                "category": "booking",
                "display_order": 1,
            },
            {
                "question": "What is your cancellation policy?",
                "answer": "Full refund if cancelled 30+ days in advance. 50% refund for 15-29 days. No refund for cancellations less than 14 days before the event.",
                "category": "payment",
                "display_order": 2,
            },
            {
                "question": "Do you provide setup and breakdown services?",
                "answer": "Yes! We handle complete setup 2-4 hours before your event and full breakdown after. This is included in all our packages.",
                "category": "delivery",
                "display_order": 3,
            },
            {
                "question": "Can I customize my package?",
                "answer": "Absolutely! All packages can be fully customized to match your theme, color scheme, and specific requirements. We also offer add-on enhancements.",
                "category": "customization",
                "display_order": 4,
            },
            {
                "question": "What forms of payment do you accept?",
                "answer": "We accept credit cards, debit cards, and bank transfers. A 30% deposit is required to secure your booking, with the balance due 7 days before the event.",
                "category": "payment",
                "display_order": 5,
            },
            {
                "question": "How far in advance should I book?",
                "answer": "We recommend booking 4-6 weeks in advance for best availability. Rush bookings may be available for an additional fee, but options may be limited.",
                "category": "booking",
                "display_order": 6,
            },
            {
                "question": "Do you serve areas outside your local region?",
                "answer": "Yes! We can travel to venues outside our standard service area. Additional travel fees may apply depending on the distance.",
                "category": "delivery",
                "display_order": 7,
            },
            {
                "question": "What's included in the free consultation?",
                "answer": "During your free consultation, we discuss your vision, budget, and preferences. We can meet in-person, via video call, or phone. We'll also provide mock-ups and design samples.",
                "category": "consultation",
                "display_order": 8,
            },
        ]

        for faq_data in faqs_data:
            faq = FAQ(**faq_data)
            self.db.add(faq)

        await self.db.commit()
        print(f"  - Created {len(faqs_data)} FAQs")


# Auto-register this seeder
registry.register(FAQSeeder)
