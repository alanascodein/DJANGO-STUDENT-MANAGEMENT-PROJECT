from django.urls import path, include 
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    path("register-student/", views.student_create, name="student_create"),
    path("students/", views.student_list, name="student_list"),
    path("courses/", views.course_list, name="course_list"),
    path("register/", views.register_user, name="register"),
    path("profile/<int:id>/", views.student_profile,),
    path("delete-student/<int:id>/", views.delete_student),
    #path("api/courses/", views.api_course_list),
    path('api/', include(router.urls)),
]
