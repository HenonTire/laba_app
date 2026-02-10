from django.shortcuts import render
import rest_framework
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Tasks, Projects, Plans, Notes
from .serializer import NotesSerializer, TaskSerializer, ProjectSerializer, UserSerializer, LoginSerializer, PlansSerializer, CountSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
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
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class NoteDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer


class TasksByProjectView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
     project_id = self.kwargs['project_id']
     return Tasks.objects.filter(
        project__id=project_id,
        user=self.request.user
    )



# api/views.py





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_view(request):
    total_projects = Projects.objects.count()
    total_tasks = Tasks.objects.count()
    total_done_tasks = Tasks.objects.filter(status='done').count()
    total_plans = Plans.objects.count()

    data = {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "total_done_tasks": total_done_tasks,
        "total_plans": total_plans,
    }

    serializer = CountSerializer(data)
    return Response(serializer.data)
