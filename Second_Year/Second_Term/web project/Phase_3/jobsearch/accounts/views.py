from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # login(request, user)  # Automatically log in the user after registration
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post', 'get'], permission_classes=[permissions.AllowAny])
    def logout(self, request):
        # Allow any user to access this endpoint, even if not authenticated
        # This fixes issues where the auth middleware might block the request
        if request.user.is_authenticated:
            logout(request)
        
        # Create response and clear all cookies related to authentication
        response = Response({'success': 'Logged out successfully'})
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        
        # Set cache-control headers to prevent caching issues
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        
        return response

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def current(self, request):
        """Return the current logged-in user's info."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
