from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Tasks, Projects
from .serializer import TaskSerializer, ProjectSerializer, UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateTask(ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class CreateProject(ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(RetrieveUpdateDestroyAPIView): 
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# q9gKngQ7pHiWsKwd
# Henon@12
