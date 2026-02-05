"""Tests unitaires pour les modèles Django."""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from grades_app.models import Grade, Student, Subject
from grades_app.tests.factories import GradeFactory, StudentFactory, SubjectFactory


# ============================================================================
# Tests du modèle Student
# ============================================================================

class TestStudentModel:
    """Tests pour le modèle Student."""

    @pytest.mark.django_db
    def test_student_creation_with_required_fields(self):
        """Créer un étudiant avec les champs obligatoires."""
        student = StudentFactory(
            first_name="Alice",
            last_name="Dupont",
            email="alice@example.com"
        )
        assert student.id is not None
        assert student.first_name == "Alice"
        assert student.last_name == "Dupont"
        assert student.email == "alice@example.com"

    @pytest.mark.django_db
    def test_student_requires_email_unique(self):
        """L'email doit être unique."""
        StudentFactory(email='unique@example.com')
        with pytest.raises(IntegrityError):
            StudentFactory(email='unique@example.com')

    @pytest.mark.django_db
    def test_student_auto_generates_matricule(self):
        """Le matricule est généré automatiquement au save."""
        student = StudentFactory()
        assert student.matricule is not None
        assert student.matricule.startswith(str(timezone.now().year))
        assert len(student.matricule) == 8

    @pytest.mark.django_db
    def test_student_matricule_is_unique(self):
        """Les matricules générés doivent être uniques."""
        student1 = StudentFactory()
        student2 = StudentFactory()
        assert student1.matricule != student2.matricule

    @pytest.mark.django_db
    def test_student_can_update_level(self):
        """Pouvoir changer le niveau d'un étudiant."""
        student = StudentFactory(level=Student.LEVEL_L1)
        student.level = Student.LEVEL_L2
        student.save()
        student.refresh_from_db()
        assert student.level == Student.LEVEL_L2

    @pytest.mark.django_db
    def test_student_all_level_choices(self):
        """Tester tous les choix de niveau disponibles."""
        for level_code, level_name in Student.LEVEL_CHOICES:
            student = StudentFactory(level=level_code)
            assert student.level == level_code

    @pytest.mark.django_db
    def test_student_str_representation(self):
        """Le __str__ doit afficher nom prénom et matricule."""
        student = StudentFactory(
            first_name="John",
            last_name="Doe"
        )
        assert "John" in str(student)
        assert "Doe" in str(student)
        assert student.matricule in str(student)

    @pytest.mark.django_db
    def test_student_created_at_auto_set(self):
        """Le champ created_at est défini automatiquement."""
        student = StudentFactory()
        assert student.created_at is not None

    @pytest.mark.django_db
    def test_student_compute_general_average_no_grades(self):
        """La moyenne générale est 0 sans notes."""
        student = StudentFactory()
        assert student.compute_general_average() == 0.0

    @pytest.mark.django_db
    def test_student_compute_general_average_single_subject(self):
        """Calcul de moyenne avec une seule matière."""
        student = StudentFactory()
        subject = SubjectFactory(coefficient=2.0)
        GradeFactory(student=student, subject=subject, value=15)
        assert student.compute_general_average() == 15.0

    @pytest.mark.django_db
    def test_student_compute_general_average_multiple_subjects(self):
        """Calcul de moyenne pondérée avec plusieurs matières."""
        student = StudentFactory()
        subject1 = SubjectFactory(coefficient=2.0)
        subject2 = SubjectFactory(coefficient=1.0)
        GradeFactory(student=student, subject=subject1, value=10)
        GradeFactory(student=student, subject=subject2, value=20)
        # (10 * 2 + 20 * 1) / (2 + 1) = 40 / 3 = 13.33
        assert student.compute_general_average() == pytest.approx(13.33, 0.01)

    @pytest.mark.django_db
    def test_student_compute_general_average_multiple_grades_same_subject(self):
        """Calcul de moyenne avec plusieurs notes par matière (dates différentes)."""
        student = StudentFactory()
        subject = SubjectFactory(coefficient=2.0)
        from django.utils import timezone
        date1 = timezone.now().date()
        date2 = timezone.now().date() - timezone.timedelta(days=1)
        GradeFactory(student=student, subject=subject, value=10, date=date1)
        GradeFactory(student=student, subject=subject, value=20, date=date2)
        # Les deux notes existent, moyenne affichée
        avg = student.compute_general_average()
        # Moyenne: (10 + 20) / 2 = 15
        assert avg == 15.0

    @pytest.mark.django_db
    def test_student_ordering_by_name(self):
        """Les étudiants sont ordonnés par nom puis prénom."""
        s1 = StudentFactory(first_name="Alice", last_name="Zebra")
        s2 = StudentFactory(first_name="Bob", last_name="Alpha")
        students = Student.objects.all()
        assert students[0].last_name == "Alpha"
        assert students[1].last_name == "Zebra"


# ============================================================================
# Tests du modèle Subject
# ============================================================================

class TestSubjectModel:
    """Tests pour le modèle Subject."""

    @pytest.mark.django_db
    def test_subject_creation_with_required_fields(self):
        """Créer une matière avec les champs obligatoires."""
        subject = SubjectFactory(
            code="MATH101",
            name="Mathématiques",
            coefficient=2.0
        )
        assert subject.code == "MATH101"
        assert subject.name == "Mathématiques"
        assert subject.coefficient == 2.0

    @pytest.mark.django_db
    def test_subject_requires_unique_code(self):
        """Le code doit être unique."""
        SubjectFactory(code='MATH1')
        with pytest.raises(IntegrityError):
            SubjectFactory(code='MATH1')

    @pytest.mark.django_db
    def test_subject_str_representation(self):
        """Le __str__ doit afficher code et nom."""
        subject = SubjectFactory(code="PHYS101", name="Physique")
        assert "PHYS101" in str(subject)
        assert "Physique" in str(subject)

    @pytest.mark.django_db
    def test_subject_ordering_by_code(self):
        """Les matières sont ordonnées par code."""
        s1 = SubjectFactory(code="ZZZ")
        s2 = SubjectFactory(code="AAA")
        subjects = Subject.objects.all()
        assert subjects[0].code == "AAA"
        assert subjects[1].code == "ZZZ"

    @pytest.mark.django_db
    def test_subject_coefficient_float(self):
        """Le coefficient peut être un nombre décimal."""
        subject = SubjectFactory(coefficient=1.5)
        assert subject.coefficient == 1.5

    @pytest.mark.django_db
    def test_subject_coefficient_can_be_zero(self):
        """Le coefficient peut techniquement être 0 (sera validé au save de Grade)."""
        subject = SubjectFactory(coefficient=0.0)
        assert subject.coefficient == 0.0


# ============================================================================
# Tests du modèle Grade
# ============================================================================

class TestGradeModel:
    """Tests pour le modèle Grade."""

    @pytest.mark.django_db
    def test_grade_creation_with_required_fields(self):
        """Créer une note avec les champs obligatoires."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = GradeFactory(
            student=student,
            subject=subject,
            value=15.5
        )
        assert grade.student == student
        assert grade.subject == subject
        assert grade.value == 15.5

    @pytest.mark.django_db
    def test_grade_validation_value_too_low(self):
        """Une note < 0 doit lever une ValidationError."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = Grade(student=student, subject=subject, value=-1)
        with pytest.raises(ValidationError):
            grade.full_clean()

    @pytest.mark.django_db
    def test_grade_validation_value_too_high(self):
        """Une note > 20 doit lever une ValidationError."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = Grade(student=student, subject=subject, value=25)
        with pytest.raises(ValidationError):
            grade.full_clean()

    @pytest.mark.django_db
    def test_grade_validation_value_valid_boundaries(self):
        """Les notes 0 et 20 sont valides."""
        student = StudentFactory()
        subject = SubjectFactory()
        
        # Note 0
        grade0 = Grade(student=student, subject=subject, value=0)
        grade0.full_clean()  # Ne doit pas lever d'exception
        
        # Note 20
        grade20 = Grade(student=student, subject=subject, value=20)
        grade20.full_clean()

    @pytest.mark.django_db
    def test_grade_validation_subject_coefficient_positive(self):
        """Si coefficient ≤ 0, lever ValidationError."""
        student = StudentFactory()
        subject = SubjectFactory(coefficient=0)
        grade = Grade(student=student, subject=subject, value=15)
        with pytest.raises(ValidationError):
            grade.full_clean()

    @pytest.mark.django_db
    def test_grade_date_auto_set(self):
        """La date est définie automatiquement à aujourd'hui."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = GradeFactory(student=student, subject=subject)
        assert grade.date == timezone.now().date()

    @pytest.mark.django_db
    def test_grade_comment_optional(self):
        """Le commentaire est optionnel."""
        grade = GradeFactory(comment="")
        assert grade.comment == ""

    @pytest.mark.django_db
    def test_grade_unique_together_constraint(self):
        """Chaque combinaison (student, subject, date) doit être unique."""
        student = StudentFactory()
        subject = SubjectFactory()
        date = timezone.now().date()
        
        GradeFactory(student=student, subject=subject, date=date)
        
        # Essayer d'ajouter une deuxième note le même jour pour la même matière
        with pytest.raises(ValidationError):
            GradeFactory(student=student, subject=subject, date=date)

    @pytest.mark.django_db
    def test_grade_str_representation(self):
        """Le __str__ doit afficher matricule, code et valeur."""
        student = StudentFactory()
        subject = SubjectFactory(code="MATH")
        grade = GradeFactory(student=student, subject=subject, value=15)
        
        result = str(grade)
        assert student.matricule in result
        assert "MATH" in result
        assert "15" in result

    @pytest.mark.django_db
    def test_grade_ordering_by_date_desc(self):
        """Les notes sont ordonnées par date décroissante."""
        student = StudentFactory()
        subject = SubjectFactory()
        
        date1 = timezone.now().date()
        date2 = timezone.now().date() - timezone.timedelta(days=1)
        
        grade1 = GradeFactory(student=student, subject=subject, date=date1)
        grade2 = GradeFactory(
            student=student, 
            subject=subject, 
            date=date2,
            value=10  # Valeur différente pour unique_together
        )
        
        grades = Grade.objects.filter(student=student, subject=subject)
        # Première en résultat doit être la plus récente
        assert grades[0].date >= grades[1].date

    @pytest.mark.django_db
    def test_grade_decimal_values(self):
        """Les notes peuvent avoir des décimales."""
        grade = GradeFactory(value=15.75)
        assert grade.value == 15.75

    @pytest.mark.django_db
    def test_grade_save_validates_before_save(self):
        """La méthode save() appelle full_clean()."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = Grade(student=student, subject=subject, value=25)
        
        with pytest.raises(ValidationError):
            grade.save()
