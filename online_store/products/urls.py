
from django.urls import path

from online_store.products.views import ProductListView, ProductDetailView, add_product

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add/", add_product, name="add_product"),
]