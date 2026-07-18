from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Course, Student
from .forms import StudentForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import CourseSerializer, StudentSerializer

from rest_framework.permissions import IsAuthenticated

def hello_world(request):
    return HttpResponse("Welcome to the University Hub!")

@login_required
def course_list(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses,
        'pagetitle': 'Available Courses'
    }
    return render(request, 'academic/course_list.html', context)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'academic/student_list.html', {'students': students})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            #form.save()
            #return redirect('course_list')
            username = request.POST.get('username','').strip()
            password = request.POST.get('password','').strip()
            email = request.POST.get('email','').strip()

            if not username or not password or not email:
                return render(request, 'academic/student_form.html', {
                    'form': form, 
                    'error': 'All fields are required.'})
            if User.objects.filter(username=username).exists():
                return render(request, 'academic/student_form.html', {
                    'form': form, 
                    'error': 'Username already exists.'})
            user = User.objects.create_user(
                username=username,
                password=password, 
                email=email)
            student = form.save(commit=False)
            student.user = user
            student.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('course_list')
    else:
        form = StudentForm()
    return render(request, 'academic/student_form.html', {'form': form})

from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request,
                  'registration/register.html',
                  {'form': form})
def is_admin(user):
    return user.is_staff
@user_passes_test(is_admin)
def delete_student(request, id):
    student = Student.objects.get(id=id)
    if student.user:
        student.user.delete()  # Delete the associated User object
    else:
        student.delete()
    return redirect('course_list')

@login_required
def student_profile(request, id):
    profile = Student.objects.get(id=id)
    if request.user != profile.user:
        return HttpResponse("Unauthorized", status=401)
    return HttpResponse("Profile Allowed")

from django.http import JsonResponse
def api_course_list(request):
    courses = Course.objects.all()
    data = {
        'count': courses.count(),
        'courses': list(courses.values('name', 'code', 'credits'))
    }
    return JsonResponse(data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated] 