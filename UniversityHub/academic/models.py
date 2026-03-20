from django.db import models
from django.contrib.auth.models import User
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head_of_dept = models.CharField(max_length=100)
    desciription = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    SEMESTER_CHOICES = [
        (1,'Semester 1'),
        (2,'Semester 2'),
        (3,'Semester 3'),
        (4,'Semester 4'),
    ]
    #Foreign key links course to department
    #on_delete=models.CASCADE ensures that if a department is deleted, all its courses are also deleted(data consistensy)


    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'     
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    enrollment_rate = models.DateField(auto_now_add=True) #Set once 0on creation
    #many to many : A student cn apick multiple cources
    courses = models.ManyToManyField(Course, blank=True)

    profile_pic = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
