from django.db import models

class ChatSession(models.Model):
    session_id  = models.CharField(max_length=100, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id}"


class Message(models.Model):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant")]
    session      = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content      = models.TextField()
    tool_used    = models.CharField(max_length=100, blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
