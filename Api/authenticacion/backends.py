from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import CustomUser, PasswordHistory  # Importa CustomUser

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Buscar al usuario por su nombre de usuario
            user = CustomUser.objects.get(username=username)  # Usa CustomUser

            # Validar que la contraseña no haya sido utilizada previamente
            if PasswordHistory.objects.filter(user=user).exists():
                for old_password in PasswordHistory.objects.filter(user=user):
                    if check_password(password, old_password.password):
                        raise ValidationError("No puedes usar una contraseña anterior.")

            # Intentar la autenticación estándar
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:  # Captura la excepción específica
            return None
        except ValidationError as e:
            raise e