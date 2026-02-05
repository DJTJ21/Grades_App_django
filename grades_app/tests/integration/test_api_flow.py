"""Tests d'intégration API - workflows complets."""
import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient

from grades_app.models import Grade, Student, Subject
from grades_app.tests.factories import GradeFactory, StudentFactory, SubjectFactory


class TestAPIAuthentication:
    """Tests de l'authentification et autorisation."""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_api_requires_authentication(self, client):
        """L'API demande l'authentification."""
        response = client.get('/api/students/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_api_accessible_with_authentication(self, client):
        """L'API est accessible avec authentification."""
        user = User.objects.create_user('testuser', 'test@example.com', 'pass')
        group, _ = Group.objects.get_or_create(name='enseignant')
        user.groups.add(group)
        
        client.force_authenticate(user=user)
        response = client.get('/api/students/')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_admin_has_full_access(self, client):
        """Un admin a accès à tous les endpoints."""
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        
        # Doit avoir accès à tous les endpoints
        assert client.get('/api/students/').status_code == 200
        assert client.get('/api/subjects/').status_code == 200
        assert client.get('/api/grades/').status_code == 200


class TestStudentAPI:
    """Tests de l'API Students."""

    @pytest.fixture
    def client(self):
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        return client

    @pytest.mark.django_db
    def test_list_students(self, client):
        """Lister les étudiants."""
        StudentFactory.create_batch(3)
        response = client.get('/api/students/')
        assert response.status_code == 200
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_create_student(self, client):
        """Créer un nouvel étudiant."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'level': 'L1',
            'email': 'john@example.com'
        }
        response = client.post('/api/students/', data)
        assert response.status_code == 201
        assert response.data['first_name'] == 'John'
        assert 'matricule' in response.data

    @pytest.mark.django_db
    def test_create_student_auto_generates_matricule(self, client):
        """La création auto-génère le matricule."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'level': 'L2',
            'email': 'jane@example.com'
        }
        response = client.post('/api/students/', data)
        assert response.status_code == 201
        assert len(response.data['matricule']) == 8

    @pytest.mark.django_db
    def test_create_student_duplicate_email_fails(self, client):
        """Créer avec un email en double doit échouer."""
        StudentFactory(email='duplicate@example.com')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'level': 'L1',
            'email': 'duplicate@example.com'
        }
        response = client.post('/api/students/', data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_retrieve_student(self, client):
        """Récupérer les détails d'un étudiant."""
        student = StudentFactory()
        response = client.get(f'/api/students/{student.id}/')
        assert response.status_code == 200
        assert response.data['id'] == student.id
        assert response.data['email'] == student.email

    @pytest.mark.django_db
    def test_update_student(self, client):
        """Mettre à jour un étudiant."""
        student = StudentFactory(level='L1')
        data = {'level': 'L2'}
        response = client.patch(f'/api/students/{student.id}/', data)
        assert response.status_code == 200
        
        student.refresh_from_db()
        assert student.level == 'L2'

    @pytest.mark.django_db
    def test_delete_student(self, client):
        """Supprimer un étudiant."""
        student = StudentFactory()
        student_id = student.id
        response = client.delete(f'/api/students/{student_id}/')
        assert response.status_code == 204
        
        assert not Student.objects.filter(id=student_id).exists()

    @pytest.mark.django_db
    def test_student_average_endpoint(self, client):
        """Endpoint de moyenne générale."""
        student = StudentFactory()
        subject1 = SubjectFactory(coefficient=2.0)
        subject2 = SubjectFactory(coefficient=1.0)
        GradeFactory(student=student, subject=subject1, value=10)
        GradeFactory(student=student, subject=subject2, value=20)
        
        response = client.get(f'/api/students/{student.id}/average/')
        assert response.status_code == 200
        assert 'general_average' in response.data
        assert response.data['general_average'] == pytest.approx(13.33, 0.01)

    @pytest.mark.django_db
    def test_student_general_average_in_list(self, client):
        """La moyenne est incluse dans la liste."""
        student = StudentFactory()
        subject = SubjectFactory()
        GradeFactory(student=student, subject=subject, value=15)
        
        response = client.get('/api/students/')
        assert response.status_code == 200
        assert response.data[0]['general_average'] == 15.0

    @pytest.mark.django_db
    def test_filter_students_by_level(self, client):
        """Filtrer les étudiants par niveau."""
        StudentFactory(level='L1')
        StudentFactory(level='L2')
        StudentFactory(level='L1')
        
        response = client.get('/api/students/?level=L1')
        assert response.status_code == 200
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_filter_students_by_matricule(self, client):
        """Filtrer les étudiants par matricule."""
        s1 = StudentFactory()
        s2 = StudentFactory()
        
        response = client.get(f'/api/students/?matricule={s1.matricule}')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['matricule'] == s1.matricule

    @pytest.mark.django_db
    def test_filter_students_by_name(self, client):
        """Filtrer les étudiants par nom."""
        StudentFactory(first_name='Alice', last_name='Dupont')
        StudentFactory(first_name='Bob', last_name='Martin')
        
        response = client.get('/api/students/?name=Alice')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['first_name'] == 'Alice'


class TestSubjectAPI:
    """Tests de l'API Subjects."""

    @pytest.fixture
    def client(self):
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        return client

    @pytest.mark.django_db
    def test_list_subjects(self, client):
        """Lister les matières."""
        SubjectFactory.create_batch(3)
        response = client.get('/api/subjects/')
        assert response.status_code == 200
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_create_subject(self, client):
        """Créer une matière."""
        data = {
            'code': 'MATH101',
            'name': 'Mathématiques',
            'coefficient': 2.0
        }
        response = client.post('/api/subjects/', data)
        assert response.status_code == 201
        assert response.data['code'] == 'MATH101'

    @pytest.mark.django_db
    def test_create_subject_duplicate_code_fails(self, client):
        """Créer avec un code en double doit échouer."""
        SubjectFactory(code='PHYS101')
        data = {
            'code': 'PHYS101',
            'name': 'Physique',
            'coefficient': 1.5
        }
        response = client.post('/api/subjects/', data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_retrieve_subject(self, client):
        """Récupérer les détails d'une matière."""
        subject = SubjectFactory()
        response = client.get(f'/api/subjects/{subject.id}/')
        assert response.status_code == 200
        assert response.data['id'] == subject.id

    @pytest.mark.django_db
    def test_update_subject(self, client):
        """Mettre à jour une matière."""
        subject = SubjectFactory(coefficient=1.0)
        data = {'coefficient': 1.5}
        response = client.patch(f'/api/subjects/{subject.id}/', data)
        assert response.status_code == 200
        
        subject.refresh_from_db()
        assert subject.coefficient == 1.5

    @pytest.mark.django_db
    def test_delete_subject(self, client):
        """Supprimer une matière."""
        subject = SubjectFactory()
        subject_id = subject.id
        response = client.delete(f'/api/subjects/{subject_id}/')
        assert response.status_code == 204
        
        assert not Subject.objects.filter(id=subject_id).exists()


class TestGradeAPI:
    """Tests de l'API Grades."""

    @pytest.fixture
    def client(self):
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        return client

    @pytest.mark.django_db
    def test_list_grades(self, client):
        """Lister les notes."""
        GradeFactory.create_batch(3)
        response = client.get('/api/grades/')
        assert response.status_code == 200
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_create_grade(self, client):
        """Créer une note."""
        student = StudentFactory()
        subject = SubjectFactory()
        data = {
            'student': student.id,
            'subject': subject.id,
            'value': 15.5,
            'comment': 'Bon travail'
        }
        response = client.post('/api/grades/', data)
        assert response.status_code == 201
        assert response.data['value'] == 15.5

    @pytest.mark.django_db
    def test_create_grade_invalid_value_too_low(self, client):
        """Créer une note < 0 doit échouer."""
        student = StudentFactory()
        subject = SubjectFactory()
        data = {
            'student': student.id,
            'subject': subject.id,
            'value': -1
        }
        response = client.post('/api/grades/', data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_grade_invalid_value_too_high(self, client):
        """Créer une note > 20 doit échouer."""
        student = StudentFactory()
        subject = SubjectFactory()
        data = {
            'student': student.id,
            'subject': subject.id,
            'value': 25
        }
        response = client.post('/api/grades/', data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_grade_valid_boundaries(self, client):
        """Notes 0 et 20 sont valides."""
        student = StudentFactory()
        subject = SubjectFactory()
        
        # Note 0
        response0 = client.post('/api/grades/', {
            'student': student.id,
            'subject': subject.id,
            'value': 0
        })
        assert response0.status_code == 201
        
        # Note 20 (avec date différente pour unique_together)
        from django.utils import timezone
        response20 = client.post('/api/grades/', {
            'student': student.id,
            'subject': subject.id,
            'value': 20,
            'date': (timezone.now().date() - timezone.timedelta(days=1)).isoformat()
        })
        assert response20.status_code == 201

    @pytest.mark.django_db
    def test_retrieve_grade(self, client):
        """Récupérer les détails d'une note."""
        grade = GradeFactory()
        response = client.get(f'/api/grades/{grade.id}/')
        assert response.status_code == 200
        assert response.data['id'] == grade.id

    @pytest.mark.django_db
    def test_update_grade(self, client):
        """Mettre à jour une note."""
        grade = GradeFactory(value=10)
        data = {'value': 15}
        response = client.patch(f'/api/grades/{grade.id}/', data)
        assert response.status_code == 200
        
        grade.refresh_from_db()
        assert grade.value == 15

    @pytest.mark.django_db
    def test_delete_grade(self, client):
        """Supprimer une note."""
        grade = GradeFactory()
        grade_id = grade.id
        response = client.delete(f'/api/grades/{grade_id}/')
        assert response.status_code == 204
        
        assert not Grade.objects.filter(id=grade_id).exists()


class TestEndToEndScenario:
    """Tests de scénarios complets end-to-end."""

    @pytest.fixture
    def client(self):
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        return client

    @pytest.mark.django_db
    @pytest.mark.integration
    def test_create_student_assign_grade_and_average(self, client):
        """Workflow complet: créer étudiant → créer matière → attribuer note → calculer moyenne."""
        # 1. Créer un étudiant
        student_resp = client.post(
            '/api/students/',
            {
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'level': 'L1',
                'email': 'jean.dupont@example.com',
            },
            format='json',
        )
        assert student_resp.status_code == 201
        student_id = student_resp.data['id']

        # 2. Créer une matière
        subject_resp = client.post(
            '/api/subjects/',
            {
                'code': 'MAT101',
                'name': 'Mathematiques',
                'coefficient': 2.0,
            },
            format='json',
        )
        assert subject_resp.status_code == 201
        subject_id = subject_resp.data['id']

        # 3. Attribuer une note
        grade_resp = client.post(
            '/api/grades/',
            {
                'student': student_id,
                'subject': subject_id,
                'value': 16.0,
            },
            format='json',
        )
        assert grade_resp.status_code == 201

        # 4. Vérifier la moyenne
        average_resp = client.get(f'/api/students/{student_id}/average/')
        assert average_resp.status_code == 200
        assert average_resp.data['general_average'] == 16.0

    @pytest.mark.django_db
    def test_complete_workflow(self, client):
        """Workflow complet: créer étudiant → créer matières → attribuer notes → calculer moyenne."""
        # 1. Créer un étudiant
        student_data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'level': 'L1',
            'email': 'alice@example.com'
        }
        student_response = client.post('/api/students/', student_data)
        assert student_response.status_code == 201
        student_id = student_response.data['id']

        # 2. Créer des matières
        subject_data_1 = {
            'code': 'MATH101',
            'name': 'Mathématiques',
            'coefficient': 2.0
        }
        subject_response_1 = client.post('/api/subjects/', subject_data_1)
        assert subject_response_1.status_code == 201
        subject1_id = subject_response_1.data['id']

        subject_data_2 = {
            'code': 'PHYS101',
            'name': 'Physique',
            'coefficient': 1.5
        }
        subject_response_2 = client.post('/api/subjects/', subject_data_2)
        assert subject_response_2.status_code == 201
        subject2_id = subject_response_2.data['id']

        # 3. Attribuer des notes
        grade_data_1 = {
            'student': student_id,
            'subject': subject1_id,
            'value': 18,
            'comment': 'Excellent travail'
        }
        grade_response_1 = client.post('/api/grades/', grade_data_1)
        assert grade_response_1.status_code == 201

        grade_data_2 = {
            'student': student_id,
            'subject': subject2_id,
            'value': 12
        }
        grade_response_2 = client.post('/api/grades/', grade_data_2)
        assert grade_response_2.status_code == 201

        # 4. Vérifier la moyenne générale
        # Moyenne pondérée: (18 * 2 + 12 * 1.5) / (2 + 1.5) = (36 + 18) / 3.5 = 54 / 3.5 = 15.43
        average_response = client.get(f'/api/students/{student_id}/average/')
        assert average_response.status_code == 200
        expected_average = (18 * 2 + 12 * 1.5) / (2 + 1.5)
        assert average_response.data['general_average'] == pytest.approx(expected_average, 0.01)

    @pytest.mark.django_db
    def test_multiple_students_multiple_subjects(self, client):
        """Test avec plusieurs étudiants et matières."""
        # Créer 2 étudiants
        students = []
        for i in range(2):
            response = client.post('/api/students/', {
                'first_name': f'Student{i}',
                'last_name': f'Name{i}',
                'level': 'L1',
                'email': f'student{i}@example.com'
            })
            students.append(response.data['id'])

        # Créer 3 matières
        subjects = []
        for i in range(3):
            response = client.post('/api/subjects/', {
                'code': f'SUB{i}',
                'name': f'Subject {i}',
                'coefficient': 1.0 + i
            })
            subjects.append(response.data['id'])

        # Attribuer des notes à chaque combinaison
        for student_id in students:
            for subject_id in subjects:
                response = client.post('/api/grades/', {
                    'student': student_id,
                    'subject': subject_id,
                    'value': 15
                })
                assert response.status_code == 201

        # Vérifier que les données sont cohérentes
        for student_id in students:
            avg_response = client.get(f'/api/students/{student_id}/average/')
            assert avg_response.status_code == 200
            assert avg_response.data['general_average'] == 15.0
