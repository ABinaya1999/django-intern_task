from django.contrib import admin
from .models import UserProfile, Task, Attendance

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

admin.site.register(UserProfile, UserProfileAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'assigned_to', 'completed']
admin.site.register(Task, TaskAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'sign_in_time', 'sign_out_time']
admin.site.register(Attendance, AttendanceAdmin)


