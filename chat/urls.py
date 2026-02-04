from django.urls import path
from .views import GlobalMessageListView

urlpatterns = [
    path("messages/", GlobalMessageListView.as_view()),
]