from django.urls import path

from .views import IndexView
from .views.price import (
    PriceCreateView,
    PriceDeleteView,
    PriceDetailView,
    PriceListView,
    PriceUpdateView,
)
from .views.product import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

urlpatterns = [
    # Index
    path("", IndexView.as_view(), name="index"),
    # Product
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/new/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    # Price
    path("price/", PriceListView.as_view(), name="price_list"),
    path("price/new/", PriceCreateView.as_view(), name="price_create"),
    path("price/<int:pk>/", PriceDetailView.as_view(), name="price_detail"),
    path("price/<int:pk>/edit/", PriceUpdateView.as_view(), name="price_edit"),
    path(
        "price/<int:pk>/delete/",
        PriceDeleteView.as_view(),
        name="price_delete",
    ),
]
