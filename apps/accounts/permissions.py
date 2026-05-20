from rest_framework.permissions import BasePermission

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
        return request.user.is_authenticated and request.user.role in ['buyer', 'vendor']

class IsOrderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user or obj.vendor.user == request.user
