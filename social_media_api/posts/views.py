from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Post, Comment
from accounts.models import User
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=404)

    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if created:
        # Create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )
        return Response({'message': 'Post liked'}, status=200)
    return Response({'message': 'Already liked'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        return Response({'message': 'Post unliked'}, status=200)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=404)
    except Like.DoesNotExist:
        return Response({'error': 'You haven’t liked this post.'}, status=400)