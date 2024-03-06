from api.apps.authentication.models.user import (
    User,
    Student,
    Teacher,
    Secretary,
)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'is_confirmed')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name',)
    search_fields = ('email', 'name')
    ordering = ('name', 'email',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'registration_id', 'created_at', 'updated_at')
    search_fields = ('user__name', 'registration_id')
    ordering = ('user__name', 'registration_id')

    class Meta:
        model = Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__name', 'user__email')
    ordering = ('user__name', 'user__email')

    class Meta:
        model = Teacher


@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__name', 'user__email')
    ordering = ('user__name', 'user__email')

    class Meta:
        model = Secretary
