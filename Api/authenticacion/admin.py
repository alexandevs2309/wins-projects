from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, Badge, Profile

# Definir un Inline para el perfil
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ['biography', 'phone', 'linkedin_profile', 'address']
    extra = 0  # No mostrar formularios vacíos adicionales

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'assigned_banca', 'access_level')  
    
    # Incluir el ProfileInline para editar el perfil en la misma vista
    inlines = [ProfileInline]
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'first_name', 'last_name')}),
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

    def biography(self, obj):
        return obj.profile.biography if obj.profile else None
    biography.short_description = 'Biografía'

    def phone(self, obj):
        return obj.profile.phone if obj.profile else None
    phone.short_description = 'Teléfono'

    def linkedin_profile(self, obj):
        return obj.profile.linkedin_profile if obj.profile else None
    linkedin_profile.short_description = 'Perfil de LinkedIn'

    def address(self, obj):
        return obj.profile.address if obj.profile else None
    address.short_description = 'Dirección'
