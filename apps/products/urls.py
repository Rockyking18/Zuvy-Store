from django.urls import path
from .views import (ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateDeleteView, VendorProductListView)

urlpatterns = [
    path('',           ProductListView.as_view(),         name='product-list'),
    path('create/',    ProductCreateView.as_view(),       name='product-create'),
    path('mine/',      VendorProductListView.as_view(),   name='vendor-products'),
    path('<int:pk>/',  ProductDetailView.as_view(),       name='product-detail'),
    path('<int:pk>/edit/', ProductUpdateDeleteView.as_view(), name='product-edit'),
]
# Mounted at: /api/products/
