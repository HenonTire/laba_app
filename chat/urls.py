from django.urls import path
from .views import RoomMessageListView

urlpatterns = [
    path(
        "rooms/<int:room_id>/messages/",
        RoomMessageListView.as_view(),
        name="room-messages"
    ),
]