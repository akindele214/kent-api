from django.shortcuts import render

from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from account.serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model

# Create your views here.

User = get_user_model()

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer