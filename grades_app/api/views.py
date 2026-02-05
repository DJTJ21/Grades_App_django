from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from grades_app.models import Grade, Student, Subject
from .permissions import RoleBasedAccess
from .serializers import GradeSerializer, StudentSerializer, SubjectSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [RoleBasedAccess]

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get('level')
        matricule = self.request.query_params.get('matricule')
        name = self.request.query_params.get('name')
        if level:
            queryset = queryset.filter(level=level)
        if matricule:
            queryset = queryset.filter(matricule__icontains=matricule)
        if name:
            queryset = queryset.filter(Q(last_name__icontains=name) | Q(first_name__icontains=name))
        return queryset

    @action(detail=True, methods=['get'])
    def average(self, request, pk=None):
        student = self.get_object()
        return Response({'student_id': student.id, 'general_average': student.compute_general_average()})


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [RoleBasedAccess]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student', 'subject')
    serializer_class = GradeSerializer
    permission_classes = [RoleBasedAccess]
