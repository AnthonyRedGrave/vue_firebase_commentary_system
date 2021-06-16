from django.urls import re_path, path

from .consumers import CommentConsumer

ws_urlpatterns = [
    path('ws/comments/', CommentConsumer.as_asgi()),
]