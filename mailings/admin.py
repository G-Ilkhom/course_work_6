from django.contrib import admin
from mailings.models import Client
from mailings.models import Message
from mailings.models import Mailing
from mailings.models import MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment')
    list_filter = ('email',)
    search_fields = ('full_name', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'content')
    list_filter = ('topic',)
    search_fields = ('content',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'frequency', 'status', 'message')
    list_filter = ('start_date',)
    search_fields = ('status', 'frequency')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_date', 'status', 'server_response', 'mailing')
    list_filter = ('attempt_date',)
    search_fields = ('server_response', 'mailing')
