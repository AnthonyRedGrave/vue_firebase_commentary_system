from rest_framework import serializers
from .models import Comment

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'date_published', 'answers', 'parent']
        