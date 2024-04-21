from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, TaskAPIView, attendance, sign_in, sign_out, mark_attendance, mark_task_complete, assign_task

router = DefaultRouter()
router.register('user-profiles', UserProfileViewSet)

urlpatterns = router.urls + [
    path('tasks/', TaskAPIView.as_view(), name='tasks'),  
    path('tasks/<int:pk>/', TaskAPIView.as_view(), name='task-detail'), 
    path('attendance/', attendance, name='attendance'),
    path('attendance/<int:pk>', attendance, name='attendance-detail'),
    
    path('sign-in/', sign_in, name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
    
    path('mark-attendance/', mark_attendance, name='mark_attendance'),
    path('mark-task-complete/', mark_task_complete, name='mark_task_complete'),
    path('assign-task/', assign_task, name='assign_task'),
]


