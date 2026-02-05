"""Tests unitaires pour les services."""
import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from grades_app.models import Student, Subject
from grades_app.services import (
    compute_subject_average,
    generate_matricule,
    validate_grade,
)
from grades_app.tests.factories import GradeFactory, StudentFactory, SubjectFactory


# ============================================================================
# Tests pour generate_matricule
# ============================================================================

class TestGenerateMatricule:
    """Tests pour la génération de matricule."""

    @pytest.mark.django_db
    def test_generate_matricule_format(self):
        """Le matricule doit avoir le format YYYYNNNN."""
        matricule = generate_matricule()
        assert len(matricule) == 8
        assert matricule[:4].isdigit()
        assert matricule[4:].isdigit()
        year_part = int(matricule[:4])
        assert year_part == timezone.now().year

    @pytest.mark.django_db
    def test_generate_matricule_starts_with_current_year(self):
        """Le matricule commence par l'année en cours."""
        matricule = generate_matricule()
        assert matricule.startswith(str(timezone.now().year))

    @pytest.mark.django_db
    def test_generate_matricule_increments_suffix(self):
        """Le suffixe s'incrémente pour chaque nouvel étudiant."""
        year = timezone.now().year
        # Créer un premier étudiant
        StudentFactory(matricule=f"{year}0001")
        mat1 = generate_matricule()
        # Créer un second étudiant avec le matricule généré
        StudentFactory(matricule=mat1)
        mat2 = generate_matricule()
        suffix1 = int(mat1[4:])
        suffix2 = int(mat2[4:])
        assert suffix2 > suffix1

    @pytest.mark.django_db
    def test_generate_matricule_with_custom_year(self):
        """La fonction peut accepter une année personnalisée."""
        matricule = generate_matricule(year=2024)
        assert matricule.startswith("2024")

    @pytest.mark.django_db
    def test_generate_matricule_is_unique(self):
        """Deux matricules générés doivent être différents."""
        year = timezone.now().year
        # Créer un premier étudiant
        mat1 = generate_matricule(year=year)
        StudentFactory(matricule=mat1)
        # Générer le second
        mat2 = generate_matricule(year=year)
        assert mat1 != mat2

    @pytest.mark.django_db
    def test_generate_matricule_for_existing_students(self):
        """Générer des matricules pour les étudiants existants."""
        StudentFactory()
        StudentFactory()
        next_matricule = generate_matricule()
        students = Student.objects.all()
        assert next_matricule not in [s.matricule for s in students]

    @pytest.mark.django_db
    def test_generate_matricule_format_and_unique(self):
        """Format du matricule et unicité."""
        year = timezone.now().year
        student = StudentFactory(matricule='')
        assert student.matricule.startswith(str(year))
        assert len(student.matricule) == 8

        student2 = StudentFactory(matricule='')
        assert student2.matricule != student.matricule

    @pytest.mark.django_db
    def test_generate_matricule_collision_increments(self):
        """En cas de collision, le suffixe s'incrémente."""
        year = timezone.now().year
        StudentFactory(matricule=f"{year}0001")
        matricule = generate_matricule(year=year)
        assert matricule == f"{year}0002"


# ============================================================================
# Tests pour validate_grade
# ============================================================================

class TestValidateGrade:
    """Tests pour la validation de notes."""

    def test_validate_grade_valid_values(self):
        """Les notes entre 0 et 20 sont valides."""
        # Ne doit pas lever d'exception
        validate_grade(0)
        validate_grade(10)
        validate_grade(20)
        validate_grade(15.5)

    def test_validate_grade_negative_value(self):
        """Une note négative lève ValidationError."""
        with pytest.raises(ValidationError):
            validate_grade(-1)

    def test_validate_grade_above_twenty(self):
        """Une note > 20 lève ValidationError."""
        with pytest.raises(ValidationError):
            validate_grade(21)

    def test_validate_grade_boundary_zero(self):
        """La note 0 est acceptée."""
        validate_grade(0)  # Ne doit pas lever

    def test_validate_grade_boundary_twenty(self):
        """La note 20 est acceptée."""
        validate_grade(20)  # Ne doit pas lever

    def test_validate_grade_decimal_values(self):
        """Les notes décimales sont acceptées."""
        validate_grade(10.5)
        validate_grade(19.99)

    def test_validate_grade_exact_message(self):
        """Le message d'erreur est approprié."""
        with pytest.raises(ValidationError) as exc_info:
            validate_grade(25)
        assert "between 0 and 20" in str(exc_info.value)

    @pytest.mark.parametrize('value', [-1, 21])
    def test_validate_grade_error(self, value):
        """Tests paramétrés pour les valeurs invalides."""
        with pytest.raises(ValidationError):
            validate_grade(value)

    def test_validate_grade_success(self):
        """Un cas de succès simple."""
        validate_grade(15.5)


# ============================================================================
# Tests pour compute_subject_average
# ============================================================================

class TestComputeSubjectAverage:
    """Tests pour le calcul de moyenne par matière."""

    @pytest.mark.django_db
    def test_compute_subject_average_no_grades(self):
        """La moyenne est 0 sans notes."""
        student = StudentFactory()
        subject = SubjectFactory()
        avg = compute_subject_average(student, subject.id)
        assert avg == 0.0

    @pytest.mark.django_db
    def test_compute_subject_average_single_grade(self):
        """La moyenne avec une seule note."""
        student = StudentFactory()
        subject = SubjectFactory()
        GradeFactory(student=student, subject=subject, value=15)
        avg = compute_subject_average(student, subject.id)
        assert avg == 15.0

    @pytest.mark.django_db
    def test_compute_subject_average_multiple_grades(self):
        """La moyenne avec plusieurs notes."""
        student = StudentFactory()
        subject = SubjectFactory()
        GradeFactory(student=student, subject=subject, value=10)
        GradeFactory(student=student, subject=subject, value=20, 
                     date=timezone.now().date() - timezone.timedelta(days=1))
        avg = compute_subject_average(student, subject.id)
        # Moyenne: (10 + 20) / 2 = 15
        assert avg == 15.0

    @pytest.mark.django_db
    def test_compute_subject_average_rounded_to_two_decimals(self):
        """La moyenne est arrondie à 2 décimales."""
        student = StudentFactory()
        subject = SubjectFactory()
        GradeFactory(student=student, subject=subject, value=10)
        GradeFactory(student=student, subject=subject, value=11,
                     date=timezone.now().date() - timezone.timedelta(days=1))
        avg = compute_subject_average(student, subject.id)
        # Moyenne: (10 + 11) / 2 = 10.5
        assert avg == 10.5

    @pytest.mark.django_db
    def test_compute_subject_average_for_other_students_not_included(self):
        """La moyenne ne compte que les notes de l'étudiant."""
        student1 = StudentFactory()
        student2 = StudentFactory()
        subject = SubjectFactory()
        
        GradeFactory(student=student1, subject=subject, value=10)
        GradeFactory(student=student2, subject=subject, value=20)
        
        avg1 = compute_subject_average(student1, subject.id)
        avg2 = compute_subject_average(student2, subject.id)
        
        assert avg1 == 10.0
        assert avg2 == 20.0

    @pytest.mark.django_db
    def test_compute_subject_average_for_specific_subject_only(self):
        """La moyenne ne compte que les notes de la matière spécifiée."""
        student = StudentFactory()
        subject1 = SubjectFactory()
        subject2 = SubjectFactory()
        
        GradeFactory(student=student, subject=subject1, value=10)
        GradeFactory(student=student, subject=subject2, value=20)
        
        avg1 = compute_subject_average(student, subject1.id)
        avg2 = compute_subject_average(student, subject2.id)
        
        assert avg1 == 10.0
        assert avg2 == 20.0
