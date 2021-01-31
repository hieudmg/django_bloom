from rest_framework import viewsets
from post.models import Post, Category
from .serializers import PostsSerializer, CategoriesSerializer
from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminUserOrReadOnly]
