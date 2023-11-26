from django.urls import path

from .views import (
    IndexView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("product/", ProductListView.as_view(), name="product_list"),
    path("product/new/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]
