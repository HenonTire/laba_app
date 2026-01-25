from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Tasks, Projects, Plans, Notes
from .serializer import NotesSerializer, TaskSerializer, ProjectSerializer, UserSerializer, LoginSerializer, PlansSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class LoginView(APIView):
    prmission_classes = []
    authentication_classes = [] 
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = User.objects.all()
    
    serializer_class = UserSerializer

class CreateTask(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

class CreateProject(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAuthenticated]
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

class UserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# q9gKngQ7pHiWsKwd
# Henon@12


class PlansList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer

class PlanDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plans.objects.all()
    serializer_class = PlansSerializer
class NotesList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
class NoteDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer