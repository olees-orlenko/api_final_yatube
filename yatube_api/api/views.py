from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from posts.models import Follow, Group, Post, User
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.permissions import IsContentAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsContentAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsContentAuthorOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsContentAuthorOrReadOnly, )

    def get_post(self):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return self.post

    def get_queryset(self):
        post = self.get_post()
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ['following__username', 'user__username']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        new_queryset = user.follower.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
