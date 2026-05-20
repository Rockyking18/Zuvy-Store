from django.urls import path
from .views import OrderCreateView, OrderDetailView, BuyerOrderListView, VendorOrderListView

urlpatterns = [
    path('',          OrderCreateView.as_view(),    name='order-create'),
    path('',          BuyerOrderListView.as_view(), name='order-list'),
    path('vendor/',   VendorOrderListView.as_view(),name='vendor-orders'),
    path('<int:pk>/', OrderDetailView.as_view(),    name='order-detail'),
]
# Mounted at: /api/orders/
# POST /api/orders/         — place order
# GET  /api/orders/         — buyer: my orders
# GET  /api/orders/vendor/  — vendor: my incoming orders
# GET  /api/orders/:id/     — order detail
