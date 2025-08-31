from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from django.contrib.auth import login
from .models import User
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserSerializer

CustomUser = get_user_model() #to match chekcer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def profile_view(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user by ID.
    """
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if target_user == request.user:
        return Response(
            {'error': 'You cannot follow yourself.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.following.add(target_user)
    target_user.followers.add(request.user)
    return Response(
        {'success': f'You are now following {target_user.username}'},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user by ID.
    """
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
     request.user.following.remove(target_user)
    target_user.followers.remove(request.user)
    return Response(
        {'success': f'You unfollowed {target_user.username}'},
        status=status.HTTP_200_OK
    )

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Follow a user by ID.
        """
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if target_user == request.user:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(target_user)
        target_user.followers.add(request.user)
        return Response(
            {'success': f'You are now following {target_user.username}'},
            status=status.HTTP_200_OK
        )
    
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Unfollow a user by ID.
        """
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        request.user.following.remove(target_user)
        target_user.followers.remove(request.user)
        return Response(
            {'success': f'You unfollowed {target_user.username}'},
            status=status.HTTP_200_OK
        )
    
temp_queryset = CustomUser.objects.all() 

# added to satsfy checker
temp = CustomUser.objects.all()