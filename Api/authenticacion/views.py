from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from authenticacion.models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated , AllowAny
from .permissions import IsAdmin
from rest_framework.parsers import MultiPartParser, FormParser


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
   
    permission_classes = [AllowAny]

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
        

        
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser , FormParser)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


        # profile_data = {
        #     'id': user.id,
        #     'email': user.email,
        #     'first_name': user.first_name,
        #     'last_name': user.last_name,
        #     'role': user.role,  # Agregar el rol
        #     'assignedBanca': user.assigned_banca,  # Acceder directamente al campo
        #     'accessLevel': user.access_level,  # Agregar el nivel de acceso
        #     'biography': user.profile.biography if hasattr(user, 'profile') else None,  # Agregar la biografía (si existe)
        #     'skills': user.profile.skills.all() if hasattr(user, 'profile') else [],  # Obtener habilidades (si existen)
        #     'badges': [{'id': badge.id, 'name': badge.name, 'type': badge.type} for badge in user.profile.badges.all()] if hasattr(user, 'profile') else [],  # Obtener badges (si existen)
        #     'phone': user.profile.phone_number if hasattr(user, 'profile') else None,  # Cambiar el nombre a 'phone'
        #     'linkedinProfile': user.profile.linkedin_profile if hasattr(user, 'profile') else None,  # Agregar el perfil de LinkedIn (si existe)
        #     'activityLog': user.profile.activity_log.all() if hasattr(user, 'profile') else []  # Obtener el historial de actividad (si existe)
        
            
        # }
        return Response(profile_data)
    
   

    def put(self, request):
        print(request.path)
        user = request.user  # Obtienes el usuario autenticado
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
      
        # Si tienes un modelo de perfil asociado:
        if hasattr(user, 'profile'):
            user.profile.phone_number = request.data.get('phone_number', user.profile.phone_number)
            user.profile.save()

          # Manejo de la contraseña
        new_password = request.data.get('new_password')  # Obtener la nueva contraseña del request
        if new_password:
            user.password = make_password(new_password)  # Hashear la nueva contraseña

        # Manejo de la autenticación de dos factores (2FA)
        two_factor_enabled = request.data.get('two_factor')
        if two_factor_enabled is not None:
            # Aquí debes implementar la lógica para activar/desactivar la 2FA
            # ...
            pass 
        
        user.save()  # Guarda los cambios del usuario
        print(user)
        return Response({'status': 'Perfil actualizado', }, status=status.HTTP_200_OK)
