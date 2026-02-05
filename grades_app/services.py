from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from .models import Student


def generate_matricule(year: int | None = None) -> str:
    from .models import Student

    year_value = year or timezone.now().year
    prefix = f"{year_value}"
    existing = (
        Student.objects.filter(matricule__startswith=prefix)
        .order_by('-matricule')
        .values_list('matricule', flat=True)
    )
    if existing:
        last = existing[0]
        suffix = int(last[-4:]) + 1
    else:
        suffix = 1
    return f"{prefix}{suffix:04d}"


def validate_grade(value: float) -> None:
    if value < 0 or value > 20:
        raise ValidationError('Grade must be between 0 and 20.')


def compute_subject_average(student: 'Student', subject_id: int) -> float:
    grades = student.grades.filter(subject_id=subject_id)
    if not grades.exists():
        return 0.0
    avg = grades.aggregate(avg_value=models.Avg('value'))['avg_value']
    return round(avg or 0.0, 2)
