from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path("",      views.index,     name="index"),
    path("chat/", views.chat_page, name="chat"),

    # REST API
    path("api/chat/",                        views.ChatAPIView.as_view(),        name="api-chat"),
    path("api/session/<str:session_id>/",    views.SessionHistoryAPIView.as_view(), name="api-session"),
    path("api/session/<str:session_id>/clear/", views.ClearSessionAPIView.as_view(),  name="api-clear"),
    path("api/health/",                      views.HealthAPIView.as_view(),      name="api-health"),
]
