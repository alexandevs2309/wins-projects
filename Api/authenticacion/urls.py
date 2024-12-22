from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from authenticacion.views import (
    ProfileView, 
    RegisterView, 
    LoginView, 
    TwoFactorToggleView, 
    VerifyTwoFactorView
)

urlpatterns = [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/', ProfileView.as_view(), name='profile'),

    # URLs con nombres más descriptivos
    path('api/two_factor/toggle/', TwoFactorToggleView.as_view(), name='toggle_two_factor'),
    path('api/two_factor/verify/', VerifyTwoFactorView.as_view(), name='verify_two_factor'),

    # Rutas para restablecer contraseña (podrían ir en un archivo aparte)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Ejemplo de inclusión de URLs de otra aplicación
    # path('api/bancas/', include('bancas.urls', namespace='bancas')),
]