from rest_framework import serializers
from .models import Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class AnswerSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(read_only=False)
    # user = UserSerializer()
    user_name = serializers.CharField(source='user')
    class Meta:
        model = Comment
        fields = ['id', 'content', 'date_published', 'parent', 'user_name']

    def create(self, data):
        print("create comment")
        print(data)
        user = User.objects.get(username= data['user'])
        comment = Comment.objects.create(content=data['content'],
                              parent= data['parent'],
                              user=user)
        return comment

class CommentSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    user_name = serializers.CharField(source='user')
    class Meta:
        model = Comment
        fields = ['id', 'content', 'date_published', 'answers', 'parent', 'user_name']
    
    