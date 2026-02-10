from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
urlpatterns = [
    
    path('login/', LoginView.as_view(), name='login'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task_detail'),
    path('create_project/', CreateProject.as_view(), name='create_project'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('plans/', PlansList.as_view(), name='plans_list'),
    path('plans/<int:pk>/', PlanDetail.as_view(), name='plan_detail'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/<int:project_id>/tasks/', TasksByProjectView.as_view()),
    path('notes/', NotesList.as_view(), name='notes_list'),
    path('notes/<int:pk>/', NoteDetail.as_view(), name='note_detail')
    # ccCC
]
