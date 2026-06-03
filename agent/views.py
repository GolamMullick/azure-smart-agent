import json
import os
from django.shortcuts      import render
from django.conf           import settings
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework        import status
from openai                import AzureOpenAI
from azure.identity        import AzureCliCredential, get_bearer_token_provider

from .models       import ChatSession, Message
from .tools        import TOOLS, execute_tool
from .serializers  import ChatRequestSerializer, MessageSerializer, ChatSessionSerializer

SYSTEM_PROMPT = """You are SmartAgent, an expert AI travel assistant powered by Azure AI.

You help users:
✈️ Search and book flights between cities
🏨 Find hotels at any destination
🌤️ Check weather conditions worldwide
📍 Get destination info, visa requirements and travel tips
📋 Plan complete trip itineraries

Always use your tools to get accurate real-time information.
When presenting results, be clear, friendly and structured.
Always confirm bookings with all details."""


def get_azure_client() -> AzureOpenAI:
    token_provider = get_bearer_token_provider(
        AzureCliCredential(),
        "https://cognitiveservices.azure.com/.default"
    )
    return AzureOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21"
    )


def run_agent(conversation: list) -> tuple[str, str | None]:
    """
    Run agent loop with tool calling.
    Returns (reply_text, tool_used_name)
    """
    client    = get_azure_client()
    tool_used = None

    while True:
        response      = client.chat.completions.create(
            model=settings.AZURE_AI_MODEL_DEPLOYMENT_NAME,
            messages=conversation,
            tools=TOOLS,
            tool_choice="auto",
            max_completion_tokens=1000
        )
        msg           = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        # Convert to dict
        msg_dict = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            msg_dict["tool_calls"] = [
                {
                    "id":   tc.id,
                    "type": "function",
                    "function": {
                        "name":      tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in msg.tool_calls
            ]
        conversation.append(msg_dict)

        # Done - no tool calls
        if finish_reason == "stop" or not msg.tool_calls:
            return msg.content or "I could not process that request.", tool_used

        # Execute tools
        for tc in msg.tool_calls:
            tool_name = tc.function.name
            tool_args = json.loads(tc.function.arguments)
            result    = execute_tool(tool_name, tool_args)
            tool_used = tool_name

            conversation.append({
                "role":         "tool",
                "tool_call_id": tc.id,
                "content":      result
            })


# ── Pages ─────────────────────────────────────────

def index(request):
    return render(request, "agent/index.html")


def chat_page(request):
    return render(request, "agent/chat.html")


# ── REST API Views ────────────────────────────────

class ChatAPIView(APIView):
    """POST /api/chat/ — Send a message to the agent."""

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data["message"]
        session_id   = serializer.validated_data["session_id"]

        # Get or create session
        session, _ = ChatSession.objects.get_or_create(session_id=session_id)

        # Build conversation history from DB
        past_messages = session.messages.all()
        conversation  = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in past_messages:
            conversation.append({"role": m.role, "content": m.content})
        conversation.append({"role": "user", "content": user_message})

        # Save user message
        Message.objects.create(session=session, role="user", content=user_message)

        try:
            reply, tool_used = run_agent(conversation)

            # Save assistant reply
            Message.objects.create(
                session=session,
                role="assistant",
                content=reply,
                tool_used=tool_used
            )

            return Response({
                "reply":     reply,
                "tool_used": tool_used,
                "status":    "ok"
            })

        except Exception as e:
            return Response(
                {"error": str(e), "status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClearSessionAPIView(APIView):
    """DELETE /api/session/<session_id>/ — Clear chat history."""

    def delete(self, request, session_id):
        try:
            session = ChatSession.objects.get(session_id=session_id)
            session.messages.all().delete()
            return Response({"status": "cleared"})
        except ChatSession.DoesNotExist:
            return Response({"status": "not found"}, status=404)


class SessionHistoryAPIView(APIView):
    """GET /api/session/<session_id>/ — Get chat history."""

    def get(self, request, session_id):
        try:
            session  = ChatSession.objects.get(session_id=session_id)
            messages = session.messages.all()
            return Response({
                "session_id": session_id,
                "messages":   MessageSerializer(messages, many=True).data
            })
        except ChatSession.DoesNotExist:
            return Response({"messages": []})


class HealthAPIView(APIView):
    """GET /api/health/ — Health check."""

    def get(self, request):
        return Response({
            "status":   "ok",
            "agent":    "SmartAgent",
            "model":    settings.AZURE_AI_MODEL_DEPLOYMENT_NAME,
            "endpoint": settings.AZURE_OPENAI_ENDPOINT,
            "tools":    [t["function"]["name"] for t in TOOLS]
        })
