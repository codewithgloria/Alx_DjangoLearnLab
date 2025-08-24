from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['title', 'content']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
class UserFeedView(generics.ListAPIView):
    """
    Display posts from users that the current user is following.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following = user.following.all()
        return Post.objects.filter(author__in=following).order_by('-created_at')