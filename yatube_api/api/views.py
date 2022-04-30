# from django.core.exceptions import PermissionDenied
from rest_framework import permissions, viewsets

from .permissions import IsOwnerOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs["post_id"])
        return post.comments.all()

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs["post_id"])
        serializer.save(
            author=self.request.user,
            post_id=post.pk
        )
