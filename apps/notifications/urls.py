from django.urls import path
from .views import NotificationListView, MarkNotificationsReadView

urlpatterns = [
    path('',      NotificationListView.as_view(),     name='notification-list'),
    path('read/', MarkNotificationsReadView.as_view(), name='notifications-read'),
]
# Mounted at: /api/notifications/
# GET  /api/notifications/      — list unread notifications
# PUT  /api/notifications/read/ — mark as read (pass ids list)
