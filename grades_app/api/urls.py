from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import GradeViewSet, StudentViewSet, SubjectViewSet

router = DefaultRouter()
router.register('students', StudentViewSet)
router.register('subjects', SubjectViewSet)
router.register('grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
