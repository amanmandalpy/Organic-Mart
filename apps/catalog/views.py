"""Catalogue pages used by the public storefront."""

from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import DetailView, ListView

from apps.catalog.models import Product
from apps.catalog.selectors import active_products, featured_categories

MINIMUM_SUGGESTION_CHARS = 2


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = active_products()
        self.query = self.request.GET.get("q", "").strip()
        self.category_slug = self.request.GET.get("category", "").strip()
        self.sort = self.request.GET.get("sort", "featured").strip()

        if self.query:
            queryset = queryset.filter(
                Q(name__icontains=self.query)
                | Q(short_description__icontains=self.query)
                | Q(description__icontains=self.query)
                | Q(organic_certification__icontains=self.query)
            )

        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)

        sort_map = {
            "price-low": "price",
            "price-high": "-price",
            "rating": "-rating_average",
            "newest": "-created_at",
            "featured": "-is_featured",
        }
        return queryset.order_by(sort_map.get(self.sort, "-is_featured"), "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = featured_categories()
        context["current_category"] = self.category_slug
        context["query"] = self.query
        context["sort"] = self.sort
        context["result_count"] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    queryset = active_products().prefetch_related("reviews")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["related_products"] = (
            active_products()
            .filter(category=product.category)
            .exclude(pk=product.pk)[:4]
        )
        context["approved_reviews"] = product.reviews.filter(is_approved=True)[:5]
        return context


@require_GET
def search_suggestions(request: HttpRequest) -> JsonResponse:
    query = request.GET.get("q", "").strip()
    if len(query) < MINIMUM_SUGGESTION_CHARS:
        return JsonResponse({"results": []})

    products = active_products().filter(name__icontains=query)[:6]
    return JsonResponse(
        {
            "results": [
                {
                    "name": product.name,
                    "url": product.get_absolute_url(),
                    "price": str(product.final_price),
                    "emoji": product.image_emoji,
                }
                for product in products
            ]
        }
    )
