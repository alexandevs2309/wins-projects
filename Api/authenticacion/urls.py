from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authenticacion.views import RegisterView, LoginView

urlpatterns = [
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
]