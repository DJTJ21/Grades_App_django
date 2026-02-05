import pytest
from django.contrib.auth.models import Group, User

from grades_app.tests.factories import GradeFactory, StudentFactory, SubjectFactory


@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def subject():
    return SubjectFactory()


@pytest.fixture
def grade(student, subject):
    return GradeFactory(student=student, subject=subject)


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser('admin', 'admin@example.com', 'pass')


@pytest.fixture
def teacher_user(db):
    user = User.objects.create_user('teacher', 'teacher@example.com', 'pass')
    group, _ = Group.objects.get_or_create(name='enseignant')
    user.groups.add(group)
    return user


@pytest.fixture
def student_user(db):
    user = User.objects.create_user('student', 'student@example.com', 'pass')
    group, _ = Group.objects.get_or_create(name='etudiant')
    user.groups.add(group)
    return user
