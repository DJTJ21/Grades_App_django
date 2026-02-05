import factory
from django.utils import timezone

from grades_app.models import Grade, Student, Subject


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    level = Student.LEVEL_L1
    email = factory.Sequence(lambda n: f"student{n}@example.com")


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    code = factory.Sequence(lambda n: f"MAT{n:03d}")
    name = factory.Faker('word')
    coefficient = 1.0


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade

    student = factory.SubFactory(StudentFactory)
    subject = factory.SubFactory(SubjectFactory)
    value = 10.0
    date = factory.LazyFunction(timezone.now)
    comment = ''
