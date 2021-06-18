from typing import List
from django.db.models import query
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView
from .serializers import AnswerSerializer, CommentSerializer
from django.shortcuts import render
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from rest_framework.permissions import *

class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(parent=None)
    
class AnswerListApiView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AnswerSerializer
    