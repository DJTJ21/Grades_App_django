from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .services import generate_matricule, validate_grade


class Student(models.Model):
    LEVEL_L1 = 'L1'
    LEVEL_L2 = 'L2'
    LEVEL_L3 = 'L3'
    LEVEL_M1 = 'M1'
    LEVEL_M2 = 'M2'

    LEVEL_CHOICES = [
        (LEVEL_L1, 'Licence 1'),
        (LEVEL_L2, 'Licence 2'),
        (LEVEL_L3, 'Licence 3'),
        (LEVEL_M1, 'Master 1'),
        (LEVEL_M2, 'Master 2'),
    ]

    matricule = models.CharField(max_length=8, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.matricule})"

    def save(self, *args, **kwargs):
        if not self.matricule:
            self.matricule = generate_matricule()
        super().save(*args, **kwargs)

    def compute_general_average(self) -> float:
        grades = self.grades.all()
        if not grades.exists():
            return 0.0
        weighted_sum = 0.0
        total_coeff = 0.0
        for grade in grades.select_related('subject'):
            weighted_sum += grade.value * grade.subject.coefficient
            total_coeff += grade.subject.coefficient
        return round(weighted_sum / total_coeff, 2) if total_coeff else 0.0


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    coefficient = models.FloatField()

    class Meta:
        ordering = ['code']

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Grade(models.Model):
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='grades', on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField(default=timezone.now)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('student', 'subject', 'date')

    def clean(self) -> None:
        validate_grade(self.value)
        if self.subject.coefficient <= 0:
            raise ValidationError('Coefficient must be positive.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.student.matricule} - {self.subject.code}: {self.value}"
