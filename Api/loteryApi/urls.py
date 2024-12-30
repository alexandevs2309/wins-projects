from django.urls import path
from . import views

urlpatterns = [
    path("api/resultados/", views.search_lottery, name="resultados"),
    path("api/search/", views.search_lottery_by_name, name="search_lottery_by_name"),
    path('api/get_lottery/' , views.get_lottery, name='get_lottery'),
    path('api/search_lottery/' , views.search_lottery, name='search_lottery'),
    
    path('api/premios-hoy', views.premios_hoy, name='premios_hoy'),
    path('api/loteria-data', views.loteria_data, name='loteria_data'),
    path('api/lotteries/', views.lotteries, name='lotteries'),
]
