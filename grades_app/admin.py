from django.contrib import admin

from .models import Grade, Student, Subject


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'last_name', 'first_name', 'level', 'email', 'created_at')
    search_fields = ('matricule', 'last_name', 'first_name', 'email')
    list_filter = ('level',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'coefficient')
    search_fields = ('code', 'name')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'date')
    list_filter = ('subject', 'date')
    search_fields = ('student__matricule', 'student__last_name')
