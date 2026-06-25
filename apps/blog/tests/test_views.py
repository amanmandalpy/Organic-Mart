from http import HTTPStatus

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogCategory, BlogPost

pytestmark = pytest.mark.django_db


def test_published_blog_post_is_visible(client):
    category = BlogCategory.objects.create(name="Guides", slug="guides")
    post = BlogPost.objects.create(
        category=category,
        title="Organic buying checklist",
        slug="organic-buying-checklist",
        excerpt="A short buying checklist for organic products.",
        content="Check certification, ingredients, seller details, and reviews.",
        status=BlogPost.Status.PUBLISHED,
        published_at=timezone.now(),
    )

    response = client.get(reverse("blog:post-detail", kwargs={"slug": post.slug}))

    assert response.status_code == HTTPStatus.OK
    assert post.title in response.content.decode()


def test_draft_blog_post_is_not_public(client):
    category = BlogCategory.objects.create(name="Drafts", slug="drafts")
    post = BlogPost.objects.create(
        category=category,
        title="Internal draft",
        slug="internal-draft",
        excerpt="Not ready yet.",
        content="Draft content.",
        status=BlogPost.Status.DRAFT,
    )

    response = client.get(reverse("blog:post-detail", kwargs={"slug": post.slug}))

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_blog_search_filters_posts(client):
    category = BlogCategory.objects.create(name="Search", slug="search")
    BlogPost.objects.create(
        category=category,
        title="Honey benefits",
        slug="honey-benefits",
        excerpt="Organic honey benefits.",
        content="Honey content.",
        status=BlogPost.Status.PUBLISHED,
        published_at=timezone.now(),
    )

    response = client.get(reverse("blog:post-list"), {"q": "honey"})

    assert response.status_code == HTTPStatus.OK
    assert "Honey benefits" in response.content.decode()
