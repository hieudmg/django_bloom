from rest_framework import serializers
from post.models import Post, Category


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
