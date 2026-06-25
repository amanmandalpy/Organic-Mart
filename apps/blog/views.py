"""Public blog pages backed by admin-managed content."""

from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from apps.blog.models import BlogCategory
from apps.blog.selectors import published_blog_posts


@require_GET
def post_list(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    posts = published_blog_posts()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    categories = BlogCategory.objects.filter(is_active=True).order_by(
        "display_order",
        "name",
    )
    return render(
        request,
        "blog/post_list.html",
        {
            "posts": posts,
            "categories": categories,
            "query": query,
            "active_category": category_slug,
        },
    )


@require_GET
def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(published_blog_posts(), slug=slug)
    related_posts = (
        published_blog_posts().filter(category=post.category).exclude(pk=post.pk)[:3]
    )
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "related_posts": related_posts},
    )
