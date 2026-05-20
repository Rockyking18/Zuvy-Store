from django.urls import path
from .views import ReviewCreateView, ProductReviewListView, VendorReviewListView

urlpatterns = [
    path('',                      ReviewCreateView.as_view(),       name='review-create'),
    path('product/<int:pk>/',     ProductReviewListView.as_view(),  name='product-reviews'),
    path('vendor/<int:pk>/',      VendorReviewListView.as_view(),   name='vendor-reviews'),
]
# Mounted at: /api/reviews/
