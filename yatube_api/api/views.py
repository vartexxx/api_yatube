from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PerformUpdateDestroyViewSet(viewsets.ModelViewSet):

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('Изменение чужого контента запрещено!')

    def destroy(self, request, pk=None, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(
            PerformUpdateDestroyViewSet,
            self
        ).destroy(request, pk, *args, **kwargs)


class PostViewSet(PerformUpdateDestroyViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(PerformUpdateDestroyViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(
            post=self.get_post(),
            author=self.request.user
        )
