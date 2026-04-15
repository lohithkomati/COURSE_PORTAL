from django.db import models
from django.contrib.auth.models import User

class StudentApplication(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    COURSE_CHOICES = [
        ('Python', 'Python'),
        ('C', 'C'),
        ('C++', 'C++'),
        ('Java', 'Java'),
        ('Machine Learning', 'Machine Learning'),
        ('Deep Learning', 'Deep Learning'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.course}"
