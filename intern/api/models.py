from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SUPERVISOR = 'Supervisor'
    INTERN = 'Intern'
    ROLE_CHOICES = [
        (SUPERVISOR, 'Supervisor'),
        (INTERN, 'Intern'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sign_in_time = models.DateTimeField(auto_now_add=True)
    sign_out_time = models.DateTimeField(null=True, blank=True)
