from rest_framework.permissions import BasePermission
from django.db import models as db_models

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'buyer'

class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
class IsBuyerOrVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['buyer','vendor']

class IsApprovedVendor(BasePermission):
    """Vendor must be approved before they can list products or view orders."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role != 'vendor':
            return False
        return hasattr(request.user, 'vendor') and request.user.vendor.status == 'approved'

class IsOrderParticipant(BasePermission):
    """Object-level: only the buyer or the vendor on an order can access it."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'buyer':
            return obj.buyer == user
        if user.role == 'vendor':
            return obj.items.filter(vendor__user=user).exists()
        return False
