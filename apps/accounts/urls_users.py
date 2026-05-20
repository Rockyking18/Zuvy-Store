from django.urls import path
from .views import MeView

urlpatterns = [
    path('me/', MeView.as_view(), name='user-me'),
]
# Mounted at: /api/users/
# GET  /api/users/me/  — view own profile
# PUT  /api/users/me/  — update own profile
# DELETE /api/users/me/ — deactivate account
