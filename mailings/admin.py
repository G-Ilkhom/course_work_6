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
    list_display = ['start_date', 'end_date', 'frequency', 'status', 'is_disabled']
    list_filter = ['frequency', 'status', 'is_disabled']
    search_fields = ['start_date', 'end_date', 'message__topic']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Manager').exists():
            return qs.filter(owner=request.user)
        return qs

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('mailings.disable_mailing'):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not obj.owner == request.user:
            return False
        return has_permission


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt_date', 'status', 'server_response', 'mailing')
    list_filter = ('attempt_date',)
    search_fields = ('server_response', 'mailing')
