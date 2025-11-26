from rest_framework import serializers
from django.conf import settings
from blog.models import Category, Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'category', 'created_at', 'image']

    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    image = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)




