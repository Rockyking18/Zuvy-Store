from django.urls import path
from .views import VendorRegisterView, VendorProfileView, VendorPublicDetailView

urlpatterns = [
    path('',          VendorRegisterView.as_view(),    name='vendor-register'),
    path('me/',       VendorProfileView.as_view(),     name='vendor-profile'),
    path('<int:pk>/', VendorPublicDetailView.as_view(),name='vendor-public'),
]
# Mounted at: /api/vendors/
