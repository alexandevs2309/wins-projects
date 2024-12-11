from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from authenticacion.permissions import IsAdmin, IsGerente
from .models import Bancas
from .serializers import BancasSerializer


class BancaListCreateView(generics.ListCreateAPIView):
    queryset = Bancas.objects.all()
    serializer_class = BancasSerializer
    

    

class ProcesarDatosBancaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsGerente]
    def post(self, request, id):
        try:
            banca = Bancas.objects.get(id=id)
            # Lógica para procesar los datos de la banca
            return Response({"mensaje": "Datos procesados correctamente."}, status=status.HTTP_200_OK)
        except Bancas.DoesNotExist:
            return Response({"error": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)


class ToggleBancaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsGerente]

    def patch(self, request, id):
        print("Authorization Header:", request.headers.get('Authorization'))

        try:
            banca = Bancas.objects.get(id=id)
            banca.activa = not banca.activa  
            banca.status = "ACTIVA" if banca.activa else "INACTIVA"
            banca.save()
            
           
            serializer = BancasSerializer(banca)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Bancas.DoesNotExist:
            return Response({"error": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)


class BancaDetailView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            banca = Bancas.objects.get(id=id)
            serializer = BancasSerializer(banca)
            return Response( serializer.data, status=status.HTTP_200_OK )
        except Bancas.DoesNotExist:
            return Response({"detail": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, id):
        self.permission_classes = [IsAuthenticated, IsAdmin | IsGerente]
        try:
            banca = Bancas.objects.get(id=id)
            serializer = BancasSerializer(banca, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Bancas.DoesNotExist:
            return Response({"detail": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self , request , id): 
        self.permission_classes = [IsAuthenticated, IsAdmin | IsGerente]
        try: 
            banca = get_object_or_404(Bancas, id=id) 
            serializer = BancasSerializer(banca, data=request.data, partial=True) 
            if serializer.is_valid(): 
                serializer.save() 
                return Response(serializer.data) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except Bancas.DoesNotExist: 
            return Response({"detail": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)


class BancaDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsGerente]
    def delete(self, request, id):
        try:
            banca = Bancas.objects.get(id=id)
            banca.delete()
            return Response({"detail": "Banca eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Bancas.DoesNotExist:
            return Response({"detail": "Banca no encontrada."}, status=status.HTTP_404_NOT_FOUND)



