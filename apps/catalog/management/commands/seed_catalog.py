"""Load starter catalogue data.

This command is intentionally idempotent: it can be run many times without
creating duplicate categories, products, or reviews.
"""

from decimal import Decimal
from typing import Any

from django.core.management.base import BaseCommand

from apps.catalog.models import Category, Product, ProductReview

CATEGORIES: list[dict[str, Any]] = [
    {
        "name": "Fruits",
        "slug": "fruits",
        "icon": "🍎",
        "description": "Fresh seasonal organic fruits sourced from verified farms.",
        "display_order": 1,
    },
    {
        "name": "Vegetables",
        "slug": "vegetables",
        "icon": "🥦",
        "description": "Everyday organic vegetables for healthy home cooking.",
        "display_order": 2,
    },
    {
        "name": "Organic Grains",
        "slug": "organic-grains",
        "icon": "🌾",
        "description": "Rice, millets, pulses, and whole grains grown responsibly.",
        "display_order": 3,
    },
    {
        "name": "Honey",
        "slug": "honey",
        "icon": "🍯",
        "description": "Raw and natural honey from trusted small producers.",
        "display_order": 4,
    },
    {
        "name": "Herbal Products",
        "slug": "herbal-products",
        "icon": "🌿",
        "description": "Herbal wellness essentials for daily natural care.",
        "display_order": 5,
    },
    {
        "name": "Spices",
        "slug": "spices",
        "icon": "🌶️",
        "description": "Aromatic organic spices with clear origin details.",
        "display_order": 6,
    },
    {
        "name": "Tea",
        "slug": "tea",
        "icon": "🍵",
        "description": "Organic green tea, herbal tea, and wellness infusions.",
        "display_order": 7,
    },
    {
        "name": "Dry Fruits",
        "slug": "dry-fruits",
        "icon": "🥜",
        "description": "Premium nuts and dry fruits for everyday nutrition.",
        "display_order": 8,
    },
]

PRODUCTS: list[dict[str, Any]] = [
    {
        "category_slug": "fruits",
        "name": "Organic Alphonso Mango Box",
        "slug": "organic-alphonso-mango-box",
        "short_description": (
            "Naturally ripened premium mangoes with farm traceability."
        ),
        "description": (
            "A seasonal box of fragrant Alphonso mangoes grown without synthetic "
            "pesticides. Perfect for family desserts, smoothies, and gifting."
        ),
        "seller_name": "Konkan Organic Farms",
        "price": Decimal("899.00"),
        "discount_percent": 12,
        "stock": 42,
        "sku": "FRU-MANGO-001",
        "package_size": "2 kg box",
        "origin": "Ratnagiri, Maharashtra",
        "organic_certification": "India Organic Certified",
        "benefits": "Rich in vitamin A\nNaturally sweet\nFarm traceable",
        "ingredients": "Fresh organic Alphonso mangoes",
        "image_emoji": "🥭",
        "rating_average": Decimal("4.80"),
        "rating_count": 126,
        "is_featured": True,
    },
    {
        "category_slug": "vegetables",
        "name": "Fresh Organic Spinach",
        "slug": "fresh-organic-spinach",
        "short_description": (
            "Tender green spinach cleaned and packed for quick cooking."
        ),
        "description": (
            "Fresh spinach leaves from certified farms, ideal for soups, dal, "
            "parathas, smoothies, and everyday meals."
        ),
        "seller_name": "Green Basket Organics",
        "price": Decimal("79.00"),
        "discount_percent": 5,
        "stock": 120,
        "sku": "VEG-SPINACH-001",
        "package_size": "250 g bunch",
        "origin": "Nashik, Maharashtra",
        "organic_certification": "PGS Organic Verified",
        "benefits": "Iron rich\nLow calorie\nFreshly harvested",
        "ingredients": "Organic spinach leaves",
        "image_emoji": "🥬",
        "rating_average": Decimal("4.50"),
        "rating_count": 84,
        "is_featured": True,
    },
    {
        "category_slug": "organic-grains",
        "name": "Organic Brown Rice",
        "slug": "organic-brown-rice",
        "short_description": "Whole grain brown rice for balanced daily meals.",
        "description": (
            "Naturally grown brown rice with bran intact for a nutty taste and "
            "better everyday nutrition."
        ),
        "seller_name": "Earth Bowl Grains",
        "price": Decimal("249.00"),
        "discount_percent": 8,
        "stock": 76,
        "sku": "GRN-RICE-001",
        "package_size": "1 kg pack",
        "origin": "Wayanad, Kerala",
        "organic_certification": "USDA Organic Equivalent",
        "benefits": "Whole grain\nHigh fibre\nNo artificial polish",
        "ingredients": "Organic brown rice",
        "image_emoji": "🍚",
        "rating_average": Decimal("4.60"),
        "rating_count": 93,
        "is_featured": True,
    },
    {
        "category_slug": "honey",
        "name": "Raw Forest Honey",
        "slug": "raw-forest-honey",
        "short_description": "Unprocessed forest honey with natural floral notes.",
        "description": (
            "Raw honey collected by trained beekeepers and packed without added "
            "sugar, preservatives, or artificial flavour."
        ),
        "seller_name": "Wild Hive Naturals",
        "price": Decimal("399.00"),
        "discount_percent": 10,
        "stock": 58,
        "sku": "HNY-FOREST-001",
        "package_size": "500 g glass jar",
        "origin": "Coorg, Karnataka",
        "organic_certification": "Residue Tested Natural Honey",
        "benefits": "No added sugar\nRaw and unheated\nNatural antioxidants",
        "ingredients": "Raw forest honey",
        "image_emoji": "🍯",
        "rating_average": Decimal("4.90"),
        "rating_count": 211,
        "is_featured": True,
    },
    {
        "category_slug": "herbal-products",
        "name": "Organic Aloe Vera Gel",
        "slug": "organic-aloe-vera-gel",
        "short_description": "Soothing aloe gel for skin hydration and cooling care.",
        "description": (
            "A gentle aloe vera gel made for daily skin care. Suitable for "
            "post-sun care, hydration, and light soothing use."
        ),
        "seller_name": "Herbal Leaf Care",
        "price": Decimal("299.00"),
        "discount_percent": 15,
        "stock": 64,
        "sku": "HRB-ALOE-001",
        "package_size": "200 ml tube",
        "origin": "Jaipur, Rajasthan",
        "organic_certification": "Certified Organic Aloe Extract",
        "benefits": "Soothes skin\nLight hydration\nCooling feel",
        "ingredients": "Organic aloe vera extract\nPurified water\nNatural stabilizer",
        "image_emoji": "🧴",
        "rating_average": Decimal("4.40"),
        "rating_count": 72,
        "is_featured": True,
    },
    {
        "category_slug": "spices",
        "name": "Organic Turmeric Powder",
        "slug": "organic-turmeric-powder",
        "short_description": "High-curcumin turmeric powder for cooking and wellness.",
        "description": (
            "Aromatic turmeric powder made from carefully dried organic turmeric "
            "rhizomes. Adds colour, flavour, and warmth to meals."
        ),
        "seller_name": "Spice Roots Collective",
        "price": Decimal("189.00"),
        "discount_percent": 7,
        "stock": 98,
        "sku": "SPC-TURMERIC-001",
        "package_size": "200 g pouch",
        "origin": "Erode, Tamil Nadu",
        "organic_certification": "India Organic Certified",
        "benefits": "High curcumin\nNatural colour\nNo artificial additives",
        "ingredients": "Organic turmeric powder",
        "image_emoji": "🟡",
        "rating_average": Decimal("4.70"),
        "rating_count": 144,
        "is_featured": True,
    },
    {
        "category_slug": "tea",
        "name": "Organic Green Tea",
        "slug": "organic-green-tea",
        "short_description": "Refreshing green tea leaves for a calm daily ritual.",
        "description": (
            "Light and refreshing organic green tea from mountain estates, packed "
            "for aroma retention and a clean finish."
        ),
        "seller_name": "Himalayan Tea House",
        "price": Decimal("349.00"),
        "discount_percent": 9,
        "stock": 51,
        "sku": "TEA-GREEN-001",
        "package_size": "100 g tin",
        "origin": "Darjeeling, West Bengal",
        "organic_certification": "Organic Tea Board Certified",
        "benefits": "Refreshing taste\nNatural antioxidants\nNo artificial flavour",
        "ingredients": "Organic green tea leaves",
        "image_emoji": "🍵",
        "rating_average": Decimal("4.50"),
        "rating_count": 66,
        "is_featured": False,
    },
    {
        "category_slug": "dry-fruits",
        "name": "Premium Organic Almonds",
        "slug": "premium-organic-almonds",
        "short_description": "Crunchy almonds for snacking, breakfast, and desserts.",
        "description": (
            "Premium organic almonds packed fresh for daily nutrition. Great for "
            "snacks, smoothies, sweets, and breakfast bowls."
        ),
        "seller_name": "Nutri Valley Organics",
        "price": Decimal("699.00"),
        "discount_percent": 11,
        "stock": 37,
        "sku": "DRY-ALMOND-001",
        "package_size": "500 g pack",
        "origin": "Himachal Pradesh",
        "organic_certification": "Organic Farm Verified",
        "benefits": "Protein rich\nHealthy fats\nPremium crunch",
        "ingredients": "Organic almonds",
        "image_emoji": "🌰",
        "rating_average": Decimal("4.60"),
        "rating_count": 118,
        "is_featured": False,
    },
]

REVIEWS: list[dict[str, Any]] = [
    {
        "reviewer_name": "Priya Sharma",
        "rating": 5,
        "title": "Fresh and trustworthy",
        "body": (
            "Packaging looked premium and the product details were easy to understand."
        ),
    },
    {
        "reviewer_name": "Amit Verma",
        "rating": 4,
        "title": "Good quality",
        "body": (
            "Great shopping experience. Certification and ingredients are "
            "clearly shown."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed OrganicMart with starter categories, products, and reviews."

    def handle(self, *args: Any, **options: Any) -> None:
        del args, options
        categories: dict[str, Category] = {}

        for payload in CATEGORIES:
            category, _created = Category.objects.update_or_create(
                slug=payload["slug"],
                defaults=payload,
            )
            categories[payload["slug"]] = category

        for payload in PRODUCTS:
            category_slug = payload["category_slug"]
            product_defaults = {
                key: value for key, value in payload.items() if key != "category_slug"
            }
            product, _created = Product.objects.update_or_create(
                sku=payload["sku"],
                defaults={**product_defaults, "category": categories[category_slug]},
            )

            for review in REVIEWS:
                ProductReview.objects.update_or_create(
                    product=product,
                    reviewer_name=review["reviewer_name"],
                    title=review["title"],
                    defaults=review,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(CATEGORIES)} categories and {len(PRODUCTS)} products."
            )
        )
