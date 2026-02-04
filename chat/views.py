from rest_framework import generics, permissions
from .models import Message
from .serializer import MessageSerializer


class GlobalMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(room_id=1).order_by("created_at")

