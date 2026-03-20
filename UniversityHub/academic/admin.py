from django.contrib import admin
from.models import Department, Course, Student

#basic admin registration
admin.site.register(Department)

#advanced admin registration with customizations


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code','name','department','credits','semester')
    list_filter = ('department','semester')
    search_fields = ('name','code',)
    

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email')
    search_fields = ('first_name','email')
    