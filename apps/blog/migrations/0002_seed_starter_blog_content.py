from django.db import migrations
from django.utils import timezone


def seed_starter_blog_content(apps, schema_editor):
    BlogCategory = apps.get_model("blog", "BlogCategory")
    BlogTag = apps.get_model("blog", "BlogTag")
    BlogPost = apps.get_model("blog", "BlogPost")

    categories = {
        "buying-guide": BlogCategory.objects.get_or_create(
            slug="buying-guide",
            defaults={
                "name": "Buying Guide",
                "description": "Practical advice for choosing trusted organic products.",
                "display_order": 1,
            },
        )[0],
        "healthy-living": BlogCategory.objects.get_or_create(
            slug="healthy-living",
            defaults={
                "name": "Healthy Living",
                "description": "Seasonal food, nutrition habits, and daily organic choices.",
                "display_order": 2,
            },
        )[0],
        "seller-stories": BlogCategory.objects.get_or_create(
            slug="seller-stories",
            defaults={
                "name": "Seller Stories",
                "description": "Stories from organic growers, makers, and sellers.",
                "display_order": 3,
            },
        )[0],
    }
    tags = {
        slug: BlogTag.objects.get_or_create(slug=slug, defaults={"name": name})[0]
        for slug, name in {
            "certification": "Certification",
            "ingredients": "Ingredients",
            "seasonal": "Seasonal",
            "small-producers": "Small Producers",
        }.items()
    }

    posts = [
        {
            "title": "How to identify genuinely organic products",
            "slug": "identify-genuinely-organic-products",
            "category": categories["buying-guide"],
            "excerpt": (
                "A practical guide to checking certifications, ingredients, "
                "and seller transparency before you buy."
            ),
            "content": (
                "Start with the certification details. A trustworthy organic product "
                "should clearly mention the certifying body, batch details, and seller "
                "information.\n\nNext, read the ingredient list. Short, specific, and "
                "recognizable ingredients are easier to verify than vague claims.\n\n"
                "Finally, check reviews, return policy, and seller response quality. "
                "A transparent marketplace makes these signals easy to find."
            ),
            "tags": [tags["certification"], tags["ingredients"]],
        },
        {
            "title": "Why seasonal fruits are better for your kitchen",
            "slug": "seasonal-fruits-better-kitchen",
            "category": categories["healthy-living"],
            "excerpt": (
                "Seasonal buying usually means fresher taste, stronger value, "
                "and produce that spends less time in storage."
            ),
            "content": (
                "Seasonal fruits are harvested closer to their natural peak, which "
                "often improves taste and texture.\n\nThey can also support better "
                "pricing because supply is more natural and storage needs are lower.\n\n"
                "For families, seasonal shopping keeps meals interesting while making "
                "fresh produce easier to plan around."
            ),
            "tags": [tags["seasonal"]],
        },
        {
            "title": "Seller story: farm honey from small producers",
            "slug": "farm-honey-small-producers",
            "category": categories["seller-stories"],
            "excerpt": (
                "How small organic sellers can explain origin, quality, "
                "and benefits clearly to earn buyer trust."
            ),
            "content": (
                "Small producers often have strong product stories, but customers need "
                "clear evidence before buying online.\n\nA good seller page should show "
                "origin, production method, ingredients, certification, and honest usage "
                "guidance.\n\nWhen these details are easy to read, customers feel more "
                "confident placing repeat orders."
            ),
            "tags": [tags["small-producers"], tags["certification"]],
        },
    ]

    now = timezone.now()
    for position, item in enumerate(posts, start=1):
        post, _ = BlogPost.objects.update_or_create(
            slug=item["slug"],
            defaults={
                "title": item["title"],
                "category": item["category"],
                "excerpt": item["excerpt"],
                "content": item["content"],
                "status": "PUBLISHED",
                "is_featured": position == 1,
                "published_at": now,
                "meta_title": item["title"],
                "meta_description": item["excerpt"],
            },
        )
        post.tags.set(item["tags"])


def remove_starter_blog_content(apps, schema_editor):
    BlogPost = apps.get_model("blog", "BlogPost")
    BlogTag = apps.get_model("blog", "BlogTag")
    BlogCategory = apps.get_model("blog", "BlogCategory")
    BlogPost.objects.filter(
        slug__in=[
            "identify-genuinely-organic-products",
            "seasonal-fruits-better-kitchen",
            "farm-honey-small-producers",
        ]
    ).delete()
    BlogTag.objects.filter(
        slug__in=["certification", "ingredients", "seasonal", "small-producers"]
    ).delete()
    BlogCategory.objects.filter(
        slug__in=["buying-guide", "healthy-living", "seller-stories"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_starter_blog_content, remove_starter_blog_content)
    ]
