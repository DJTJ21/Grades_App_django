from rest_framework import serializers

from grades_app.models import Grade, Student, Subject
from grades_app.services import validate_grade


class StudentSerializer(serializers.ModelSerializer):
    general_average = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'matricule',
            'first_name',
            'last_name',
            'level',
            'email',
            'created_at',
            'general_average',
        ]
        read_only_fields = ['matricule', 'created_at', 'general_average']

    def get_general_average(self, obj: Student) -> float:
        return obj.compute_general_average()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'coefficient']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'value', 'date', 'comment']

    def validate_value(self, value: float) -> float:
        validate_grade(value)
        return value
