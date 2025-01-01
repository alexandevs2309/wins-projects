from django.urls import re_path
from .consumers import LotteryConsumer

websocket_urlpatterns = [
    re_path(r'ws/lottery/$', LotteryConsumer.as_asgi()),
]
