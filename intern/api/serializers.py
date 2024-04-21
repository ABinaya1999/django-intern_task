from rest_framework import serializers
from .models import UserProfile, Task, Attendance
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SignOutSerializer(serializers.Serializer):
    username = serializers.CharField()
