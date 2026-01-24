from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])  # 🔐 HASHING
        user.save()
        return user



from rest_framework import serializers
from .models import Tasks, Projects
from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    # 🔁 nested output only (read-only)
    user = serializers.StringRelatedField(read_only=True)
    project = ProjectSerializer(many=True, read_only=True)

    # ⬇️ input-only field for project IDs
    project_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Tasks
        fields = "__all__"
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        request = self.context.get("request")

        if request is None or request.user.is_anonymous:
            raise serializers.ValidationError("Authentication required.")

        # ✅ take user from request, not payload
        user = request.user

        # ⬇️ pop project_ids before model creation
        project_ids = validated_data.pop("project_ids", [])

        # ✅ create task with request.user
        task = Tasks.objects.create(user=user, **validated_data)

        # ✅ attach projects (many-to-many)
        if project_ids:
            projects = Projects.objects.filter(id__in=project_ids)
            task.project.set(projects)

        return task

    



class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])  # 🔐 HASHING
        user.save()
        return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# {

#     "username": "henon",
#     "password": "testing321",  
#     "email": "henontireso@gmail.com"
# }

class PlansSerializer(ModelSerializer):
    tasks = TaskSerializer(many=False)
    class Meta:
        model = Plans
        fields = '__all__'
        read_only_fields = ['id']

class NotesSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user']