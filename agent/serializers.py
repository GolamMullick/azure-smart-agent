from rest_framework import serializers
from .models import ChatSession, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Message
        fields  = ["id", "role", "content", "tool_used", "created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model  = ChatSession
        fields = ["id", "session_id", "created_at", "updated_at", "messages"]


class ChatRequestSerializer(serializers.Serializer):
    message    = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100, required=False, default="default")
