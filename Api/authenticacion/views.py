from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from authenticacion.models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdmin
from rest_framework.parsers import MultiPartParser, FormParser
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.http import HttpResponse
import qrcode

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data

        # Optimización: Actualizar el perfil usando el método update
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.phone = data.get('phone', profile.phone)
            profile.address = data.get('address', profile.address)
            profile.biography = data.get('biography', profile.biography)
            profile.linkedin_profile = data.get('linkedin_profile', profile.linkedin_profile)
            profile.save()

        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)

        new_password = request.data.get('new_password')
        if new_password:
            user.password = make_password(new_password)

        two_factor_enabled = request.data.get('two_factor')
        if two_factor_enabled is not None:
            if two_factor_enabled:
                user.enable_two_factor()
            else:
                user.disable_two_factor()

        user.save()
        return Response({'status': 'Perfil actualizado'}, status=status.HTTP_200_OK)



class RegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Usuario Registrado Correctamente",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            print("Datos recibidos:", request.data)
            response = super().post(request, *args, **kwargs)
        except Exception as e:  # Captura una excepción genérica
            import traceback
            print("Error completo en login:")
            traceback.print_exc()
            return Response({
                "error": str(e),
                "details": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        access_token = AccessToken(response.data['access'])
        user_id = access_token['user_id']

        user = CustomUser.objects.get(id=user_id)  # No es necesario el try-except aquí
        user_serializer = UserSerializer(user)
        response.data['user'] = user_serializer.data

        if user.role == 'ADMIN':
            response.data['role_message'] = "Bienvenido Administrador"
        elif user.role == 'GERENTE':
            response.data['role_message'] = "Bienvenido Gerente"
        else:
            response.data['role_message'] = "Bienvenido Empleado"

        return response



class TwoFactorToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            # Crea un nuevo dispositivo TOTP si no existe, o recupera el existente
            device = TOTPDevice.objects.get_or_create(user=user)[0]  
            otp_url = device.config_url

            # Generar el código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4,
            )
            qr.add_data(otp_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Crear respuesta HTTP con la imagen
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response
        
        except TOTPDevice.DoesNotExist:
            return Response({'message': '2FA no está habilitado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def post(self, request):
        user = request.user
        enable_2fa = request.data.get('enable_2fa', False)

        try:
            if enable_2fa:
                if not user.two_factor_enabled:
                    device = TOTPDevice.objects.get_or_create(user=user)[0]
                    user.two_factor_enabled = True
                    user.save()
                    return Response({'message': '2FA habilitado. Autenticación de dos factores actualizada'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': '2FA ya está habilitado.  '}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.two_factor_enabled:
                    user.disable_two_factor()
                    return Response({'message': '2FA deshabilitado. Autenticación de dos factores actualizada'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': '2FA ya está deshabilitado.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyTwoFactorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get('code', '')

        device = TOTPDevice.objects.get(user=user)
        if device.verify_token(code):
            return Response({"message": "Código verificado correctamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Código incorrecto o expirado."}, status=status.HTTP_400_BAD_REQUEST)