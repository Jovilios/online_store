
from django.urls import path

from online_store.products.views import ProductListView, ProductDetailView, add_product, edit_product, delete_product

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/edit/", edit_product, name="product_edit"),
    path("<int:pk>/delete/", delete_product, name="product_delete"),
    path("add/", add_product, name="add_product"),
]