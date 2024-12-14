from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, Badge

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'assigned_banca', 'access_level')  
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'first_name', 'last_name', 'profilePicture')}),
        ('Permisos', {
            'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Información Adicional', {
            'fields': ('assigned_banca', 'access_level', 'skill', 'badges')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'role'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
