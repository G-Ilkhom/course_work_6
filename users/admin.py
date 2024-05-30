from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_blocked')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_blocked')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'country', 'avatar', 'token', 'is_blocked')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_blocked')}
         ),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Manager').exists():
            return qs.filter(is_staff=False)
        return qs

    def has_perm(self, request, obj=None):
        if obj is None:
            return request.user.has_perm('users.block_users')
        return request.user.has_perm('users.block_users') and not obj.is_superuser


admin.site.register(User, CustomUserAdmin)
