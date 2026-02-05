"""Script de population des données de test."""
from django.contrib.auth.models import User, Group
from grades_app.models import Student, Subject, Grade
from django.utils import timezone

# Create groups if they don't exist
teacher_group, _ = Group.objects.get_or_create(name='enseignant')
student_group, _ = Group.objects.get_or_create(name='etudiant')

# Create sample students
students_data = [
    {'first_name': 'Jean', 'last_name': 'Dupont', 'level': 'L1', 'email': 'jean.dupont@example.com'},
    {'first_name': 'Marie', 'last_name': 'Martin', 'level': 'L2', 'email': 'marie.martin@example.com'},
    {'first_name': 'Pierre', 'last_name': 'Bernard', 'level': 'L3', 'email': 'pierre.bernard@example.com'},
    {'first_name': 'Sophie', 'last_name': 'Laurent', 'level': 'M1', 'email': 'sophie.laurent@example.com'},
    {'first_name': 'Luc', 'last_name': 'Leblanc', 'level': 'M2', 'email': 'luc.leblanc@example.com'},
]

students = []
for data in students_data:
    student, created = Student.objects.get_or_create(email=data['email'], defaults=data)
    students.append(student)
    if created:
        print(f"✓ Étudiant créé: {student}")

# Create sample subjects
subjects_data = [
    {'code': 'MATH101', 'name': 'Mathématiques Fondamentales', 'coefficient': 2.0},
    {'code': 'PHYS101', 'name': 'Physique I', 'coefficient': 1.5},
    {'code': 'PROG101', 'name': 'Introduction à la Programmation', 'coefficient': 2.0},
    {'code': 'CHI101', 'name': 'Chimie Générale', 'coefficient': 1.5},
    {'code': 'ENG101', 'name': 'Anglais Scientifique', 'coefficient': 1.0},
]

subjects = []
for data in subjects_data:
    subject, created = Subject.objects.get_or_create(code=data['code'], defaults=data)
    subjects.append(subject)
    if created:
        print(f"✓ Matière créée: {subject}")

# Create sample grades
if not Grade.objects.exists():
    for student in students:
        for subject in subjects:
            # Generate a somewhat random but consistent grade
            base_grade = 10 + (hash(f"{student.id}{subject.id}") % 100) / 10
            grade, created = Grade.objects.get_or_create(
                student=student,
                subject=subject,
                date=timezone.now().date(),
                defaults={'value': min(20, max(0, base_grade)), 'comment': 'Note initiale'}
            )
            if created:
                print(f"✓ Note créée: {grade}")

print("\n✅ Données de test chargées avec succès!")
