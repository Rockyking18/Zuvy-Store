from django.urls import path
from .views import (
    AdminVendorListView, AdminVendorStatusView,
    AdminUserListView, AdminOrderListView,
    AdminOrderRefundView, AdminCheckpointOverrideView,
    AdminStatsView, AdminSettingsView,
)

urlpatterns = [
    # Vendors
    path('vendors/',                    AdminVendorListView.as_view(),        name='admin-vendors'),
    path('vendors/<int:pk>/status/',    AdminVendorStatusView.as_view(),      name='admin-vendor-status'),
    # Users
    path('users/',                      AdminUserListView.as_view(),          name='admin-users'),
    # Orders
    path('orders/',                     AdminOrderListView.as_view(),         name='admin-orders'),
    path('orders/<int:pk>/refund/',     AdminOrderRefundView.as_view(),       name='admin-refund'),
    path('orders/<int:order_id>/checkpoints/<int:cp_id>/',
                                        AdminCheckpointOverrideView.as_view(),name='admin-cp-override'),
    # Platform
    path('stats/',                      AdminStatsView.as_view(),             name='admin-stats'),
    path('settings/',                   AdminSettingsView.as_view(),          name='admin-settings'),
]
# Mounted at: /api/admin/
# All routes protected by IsAdmin permission class
