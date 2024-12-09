from django.urls import path
from .views import BancaDeleteView, BancaDetailView, BancaListCreateView, ToggleBancaAPIView 

urlpatterns = [
    path('api/bancas/', BancaListCreateView.as_view(), name='banca-list-create'),
    path('api/bancas/<int:id>/', BancaDetailView.as_view(), name='banca-detail'),
    path('api/bancas/<int:id>/toggle/', ToggleBancaAPIView.as_view(), name='banca-toggle'),
    path('api/bancas/<int:id>/eliminar/' , BancaDeleteView.as_view(), name='eliminar_banca')
    # path('api/bancas/<int:pk>/procesar/', BancaDetailView.as_view(), name='banca-procesar'),
]
