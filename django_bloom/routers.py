from rest_framework import routers
from bloom.viewsets import PostsViewSet, CategoriesViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet)
router.register(r'categories', CategoriesViewSet)
