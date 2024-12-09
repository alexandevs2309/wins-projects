from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from authenticacion.models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin


class RegisterView(APIView):
    permission_classes = [IsAuthenticated ,IsAdmin]
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
   
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            print("Datos recibidos:", request.data)
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            import traceback
            print("Error completo en login:")
            traceback.print_exc()
            return Response({
                "error": str(e),
                "details": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        access_token = AccessToken(response.data['access'])       
        user_id = access_token['user_id']
        
        try:
            user = CustomUser.objects.get(id=user_id)
            user_serializer = UserSerializer(user)
            response.data['user'] = user_serializer.data

            if user.role == 'ADMIN':
                # Acceso especial para admin (si lo necesitas)
                response.data['role_message'] = "Bienvenido Administrador"
            elif user.role == 'GERENTE':
                # Acceso especial para gerentes
                response.data['role_message'] = "Bienvenido Gerente"
            else:
                # Para otros roles
                response.data['role_message'] = "Bienvenido Empleado"


            return response
        except Exception as e:
            import traceback
            print("Error completo en login:")
            traceback.print_exc()
            return Response({
                "error": str(e),
                "details": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)