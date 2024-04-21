from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, Task, Attendance
from .serializers import UserProfileSerializer, TaskSerializer, AttendanceSerializer, SignInSerializer, SignOutSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [BasicAuthentication]

class TaskAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                instance = Task.objects.get(pk=pk)
                serializer = TaskSerializer(instance)
                return Response(serializer.data)
            except Task.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = Task.objects.all()
            serializer = TaskSerializer(data, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            instance = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(instance, data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def attendance(request,pk=None):

    if request.method == 'GET':
        if pk:
            try:
                instance = Attendance.objects.get(pk=pk)
                serializer = AttendanceSerializer(instance)
                return Response(serializer.data)
            except Attendance.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = Attendance.objects.all()
            serializer = AttendanceSerializer(data, many=True)
            return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            instance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            instance = Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['POST'])
def sign_in(request):
    serializer = SignInSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user:
            login(request, user)
            return Response({'message': 'Sign in successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sign_out(request):
        logout(request)
        return Response({'message': 'Sign out successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    supervisor_profile = UserProfile.objects.get(user=request.user)
    if supervisor_profile.role != UserProfile.INTERN:
        return Response({'error': 'Attendance for intern only'}, status=status.HTTP_403_FORBIDDEN)
    attendance_data = {'user': request.user.id}
    serializer = AttendanceSerializer(data=attendance_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_task_complete(request):
    task_id = request.data.get('task_id')
    supervisor_profile = UserProfile.objects.get(user=request.user)
    if supervisor_profile.role != UserProfile.INTERN:
        return Response({'error': 'Intern can mark complete'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        task = Task.objects.get(pk=task_id, assigned_to=request.user)
        task.completed = True
        task.save()
        return Response({'message': 'Task marked as complete'}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found or not assigned to you'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_task(request):
    try:
        intern_username = request.data.get('intern_username')
        intern_user = User.objects.get(username=intern_username)
        task_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'assigned_to': intern_user.pk
        }
        serializer = TaskSerializer(data=task_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except:
        return Response({'details': 'No Task added'}, status=status.HTTP_404_NOT_FOUND)
