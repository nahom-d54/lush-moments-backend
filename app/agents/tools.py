"""
Database tools for Lush Moments AI Agent
"""

from contextvars import ContextVar

from langchain_core.tools import tool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import FAQ, GalleryItem, Package, PackageEnhancement, Testimonial, Theme

# Context variable to store the database session for tools
_db_session: ContextVar[AsyncSession] = ContextVar("db_session")


@tool
async def get_packages_info() -> str:
    """
    Get information about all available event decoration packages.
    Returns package names, descriptions, and pricing.
    Use this for general package inquiries.
    """
    db_session = _db_session.get()
    result = await db_session.execute(select(Package))
    packages = result.scalars().all()

    if not packages:
        return "No packages are currently available."

    info = "Available Event Decoration Packages:\n\n"
    for pkg in packages:
        info += f"**{pkg.title}** - ${pkg.price}  \n"
        if pkg.description:
            info += f"{pkg.description}  \n"
        info += "\n"

    return info


@tool
async def get_package_by_name(package_name: str) -> str:
    """
    Get detailed information about a specific package by name.
    Use this when customer asks about a specific package like "starter", "ultimate", "deluxe", etc.

    Args:
        package_name: The name of the package to search for (e.g., "starter", "ultimate", "premium")
    """
    db_session = _db_session.get()

    # Case-insensitive search with eager loading of items
    result = await db_session.execute(
        select(Package)
        .options(selectinload(Package.items))
        .where(Package.title.ilike(f"%{package_name}%"))
    )
    packages = result.scalars().all()

    if not packages:
        return f"I couldn't find a package matching '{package_name}'. Let me show you all available packages instead."

    if len(packages) == 1:
        pkg = packages[0]
        info = f"**{pkg.title}** - ${pkg.price}\n\n"
        if pkg.description:
            info += f"{pkg.description}\n\n"

        # Get package items if available (now safely loaded)
        if pkg.items:
            info += "**What's Included:**\n"
            for item in pkg.items:
                info += f"- {item.item_text}  \n"

        return info
    else:
        # Multiple matches
        info = f"I found multiple packages matching '{package_name}':\n\n"
        for pkg in packages:
            info += f"**{pkg.title}** - ${pkg.price}  \n"
            if pkg.description:
                info += f"{pkg.description}  \n"
            info += "\n"
        return info


@tool
async def get_packages_by_price(max_price: float) -> str:
    """
    Get packages within a specific price range and suggest the best value.
    Use this when customer asks about budget, affordable options, or packages under a certain price.

    Args:
        max_price: Maximum price the customer is willing to spend (e.g., 500, 1000, 2000)
    """
    db_session = _db_session.get()

    # Get all packages ordered by price
    result = await db_session.execute(select(Package).order_by(Package.price))
    all_packages = result.scalars().all()

    # Filter packages within budget
    within_budget = [pkg for pkg in all_packages if pkg.price <= max_price]

    # Find the closest package above budget for comparison
    above_budget = [pkg for pkg in all_packages if pkg.price > max_price]
    next_option = above_budget[0] if above_budget else None

    if not within_budget:
        info = (
            f"Unfortunately, we don't have any packages within ${max_price:.0f}.  \n\n"
        )
        if all_packages:
            cheapest = all_packages[0]
            info += f"Our most affordable option is the **{cheapest.title}** at ${cheapest.price:.0f}.  \n"
            if cheapest.description:
                info += f"{cheapest.description}  \n"
        return info

    info = f"**Packages within your ${max_price:.0f} budget:**\n\n"

    # Show packages within budget
    for pkg in within_budget:
        info += f"**{pkg.title}** - ${pkg.price:.0f}  \n"
        if pkg.description:
            info += f"{pkg.description}  \n"
        info += "\n"

    # Recommend the best value (highest priced within budget)
    best_value = within_budget[-1]  # Last one (highest price within budget)
    info += (
        f"**💡 Recommended:** The **{best_value.title}** at ${best_value.price:.0f} "
    )
    info += f"offers the best value within your budget.  \n\n"

    # Show next tier option if available
    if next_option:
        info += f"*For ${next_option.price:.0f}, you could upgrade to the **{next_option.title}** "
        info += f"(${next_option.price - max_price:.0f} over budget).*  \n\n"

    info += "Would you like more details about any of these packages?"

    return info


@tool
async def get_themes_info() -> str:
    """
    Get information about all available decoration themes.
    Returns theme names and descriptions.
    Use this for general theme inquiries.
    """
    db_session = _db_session.get()
    result = await db_session.execute(select(Theme))
    themes = result.scalars().all()

    if not themes:
        return "No themes are currently available."

    info = "Available Decoration Themes:\n\n"
    for theme in themes:
        info += f"**{theme.name}**  \n"
        info += f"{theme.description}  \n\n"

    return info


@tool
async def get_theme_by_name(theme_name: str) -> str:
    """
    Get detailed information about a specific theme by name.
    Use this when customer asks about a specific theme like "romantic", "vintage", "modern", etc.

    Args:
        theme_name: The name of the theme to search for
    """
    db_session = _db_session.get()

    # Case-insensitive search
    result = await db_session.execute(
        select(Theme).where(Theme.name.ilike(f"%{theme_name}%"))
    )
    themes = result.scalars().all()

    if not themes:
        return f"I couldn't find a theme matching '{theme_name}'. Let me show you all available themes instead."

    if len(themes) == 1:
        theme = themes[0]
        info = f"**{theme.name}**\n\n"
        if theme.description:
            info += f"{theme.description}\n\n"
        if hasattr(theme, "gallery_images") and theme.gallery_images:
            info += f"This theme has {len(theme.gallery_images)} gallery images available.  \n"
        return info
    else:
        info = f"I found multiple themes matching '{theme_name}':\n\n"
        for theme in themes:
            info += f"**{theme.name}**  \n"
            info += f"{theme.description}  \n\n"
        return info


@tool
async def get_gallery_items(limit: int = 5) -> str:
    """
    Get recent gallery items showcasing past event decorations.
    Use this to show examples of previous work.
    Args:
        limit: Number of gallery items to return (default 5)
    """
    db_session = _db_session.get()
    result = await db_session.execute(select(GalleryItem).limit(limit))
    items = result.scalars().all()

    if not items:
        return "No gallery items are currently available."

    info = f"Recent Event Decoration Examples (showing {len(items)}):\n\n"
    for item in items:
        info += f"**{item.title}**  \n"
        info += f"{item.description}  \n"
        if item.category:
            info += f"Category: {item.category}  \n"
        info += "\n"

    return info


@tool
async def get_testimonials(limit: int = 3) -> str:
    """
    Get customer testimonials and reviews.
    Use this when customers ask about reviews or past experiences.
    Args:
        limit: Number of testimonials to return (default 3)
    """
    db_session = _db_session.get()
    result = await db_session.execute(select(Testimonial).limit(limit))
    testimonials = result.scalars().all()

    if not testimonials:
        return "No testimonials are currently available."

    info = f"Customer Testimonials (showing {len(testimonials)}):\n\n"
    for t in testimonials:
        info += f"**{t.client_name}** - {t.event_type}  \n"
        info += f'"{t.message}"  \n'
        if t.rating:
            info += f"Rating: {'⭐' * t.rating}  \n"
        info += "\n"

    return info


@tool
async def get_booking_info() -> str:
    """
    Get information about how to book an event or consultation.
    Use this when customers ask about booking process or availability.
    """
    return """**How to Book with Lush Moments:**

1. **Browse Packages**: Choose from our Essential, Deluxe, or Signature packages  
2. **Select Theme**: Pick a theme that matches your event style  
3. **Fill Booking Form**: Provide event details (date, venue, guest count)  
4. **Consultation**: We'll schedule a free consultation to discuss your vision  
5. **Confirmation**: Receive a detailed quote and confirm your booking

**Booking Timeline:**
- We recommend booking 4-6 weeks in advance for best availability  
- Rush bookings (less than 2 weeks) may be available with limited options  
- Peak seasons (holidays, summer) book up quickly

**What You'll Need:**
- Event date and time  
- Venue location  
- Approximate guest count  
- Budget range  
- Theme preferences

You can book directly through our website's booking page or request to speak with a human agent for personalized assistance."""


@tool
async def search_faq(query: str) -> str:
    """
    Search frequently asked questions about Lush Moments services.
    Use this for general questions about services, policies, etc.
    Args:
        query: The question or topic to search for
    """
    db_session = _db_session.get()

    try:
        # Search in both questions and answers
        result = await db_session.execute(
            select(FAQ)
            .where(FAQ.is_active.is_(True))
            .where(
                (FAQ.question.ilike(f"%{query}%")) | (FAQ.answer.ilike(f"%{query}%"))
            )
            .order_by(FAQ.display_order)
            .limit(5)
        )
        faqs = result.scalars().all()

        if not faqs:
            return """For specific questions not covered in our FAQ, I recommend:

1. Requesting to speak with a human agent for personalized assistance  
2. Visiting our website for detailed information  
3. Contacting us directly via phone or email"""

        info = "Here are the answers to your questions:  \n\n"
        for faq in faqs:
            info += f"**Q: {faq.question}**  \n"
            info += f"A: {faq.answer}  \n\n"

        return info

    except Exception as e:
        return f"Error searching FAQs: {str(e)}"


@tool
async def get_package_enhancements(category: str | None = None) -> str:
    """
    Get available package enhancements and add-ons that customers can add to make their celebration more special.
    Use this when customers ask about extras, add-ons, or want to enhance their package.

    Args:
        category: Optional category filter (floral, entertainment, decor, food, furniture)

    Returns:
        str: List of available enhancements with descriptions and prices
    """
    db_session = _db_session.get()

    try:
        query = select(PackageEnhancement).where(
            PackageEnhancement.is_available.is_(True)
        )

        if category:
            query = query.where(PackageEnhancement.category == category.lower())

        query = query.order_by(PackageEnhancement.display_order)

        result = await db_session.execute(query)
        enhancements = result.scalars().all()

        if not enhancements:
            return "No enhancements available at the moment. Please check back later or contact us for custom options."

        info = "**Enhance Your Package**  \n"
        info += "Add these extras to make your celebration even more special:  \n\n"

        # Group by category
        categories = {}
        for enhancement in enhancements:
            cat = enhancement.category.title()
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(enhancement)

        for cat, items in categories.items():
            info += f"**{cat}:**  \n"
            for item in items:
                info += (
                    f"• **{item.name}** - Starting at ${item.starting_price:.0f}  \n"
                )
                info += f"  {item.description}  \n\n"

        info += "💡 *These enhancements can be added to any package. Prices may vary based on your specific needs.*  \n"

        return info

    except Exception as e:
        return f"Error retrieving package enhancements: {str(e)}"


# Export all tools
TOOLS = [
    get_packages_info,
    get_package_by_name,
    get_packages_by_price,
    get_themes_info,
    get_theme_by_name,
    get_gallery_items,
    get_testimonials,
    get_booking_info,
    search_faq,
    get_package_enhancements,
]
