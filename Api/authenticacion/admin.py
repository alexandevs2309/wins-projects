from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'assigned_banca', 'access_level')  # Elimina la coma al final
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'first_name', 'last_name', 'profile_picture', 'phone_number', 'linkedin_profile')}), 
        ('Permisos', { 'fields': ( 'role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (
            ('Información Adicional', {'fields': ('assigned_banca', 'access_level', 'biography', 'profile_picture', 'phone_number', 'linkedin_profile')}),
        )
        return fieldsets