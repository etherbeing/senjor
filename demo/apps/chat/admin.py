from django.contrib import admin

from .models import ChatRoom, Message


# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # type: ignore
    list_display = (
        "id",
        "sender",
        "content",
        "receiver",
    )
    search_fields = ("content", "sender__username", "receiver__username")
    list_filter = ("chatroom", "sender")
