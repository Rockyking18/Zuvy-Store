from django.urls import path
from .views import ProductSearchView

urlpatterns = [
    path('', ProductSearchView.as_view(), name='product-search'),
]
# Mounted at: /api/search/
# GET /api/search/?q=shoes&category=3&min_price=10&max_price=200
