from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

from django.urls import include, path

from .views import PostViewSet, GroupViewSet, CommentViewSet


router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(
    r'^posts/(?P<post_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
