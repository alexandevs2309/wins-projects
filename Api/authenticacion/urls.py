from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authenticacion.views import (ProfileView, RegisterView, LoginView, TwoFactorToggleView ,VerifyTwoFactorView)

urlpatterns = [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/' , ProfileView.as_view() , name='profile'),

    path('api/2fa/toggle/' , TwoFactorToggleView.as_view(), name='toggle_2fa'),
    path('api/2fa/verify/', VerifyTwoFactorView.as_view(), name='verify_2fa'),
]