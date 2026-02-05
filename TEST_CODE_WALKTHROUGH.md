# 🔍 Guide Code par Étape - Comprendre les Tests

## Table des Matières
1. [Étape 1: Créer une Factory](#étape-1)
2. [Étape 2: Créer une Fixture](#étape-2)
3. [Étape 3: Écrire un test unitaire](#étape-3)
4. [Étape 4: Écrire un test d'intégration](#étape-4)
5. [Étape 5: Utiliser les assertions](#étape-5)
6. [Étape 6: Tester les exceptions](#étape-6)
7. [Code complet commenté](#code-complet)

---

## Étape 1: Créer une Factory

### Qu'est-ce qu'on va faire?
Créer une factory qui génère des Student avec des données aléatoires et uniques.

### Code complet commenté

```python
# Fichier: grades_app/tests/factories.py

import factory
from django.utils import timezone
from grades_app.models import Student, Subject, Grade


# ┌─────────────────────────────────────────────────────────────┐
# │ FACTORY POUR LE MODÈLE STUDENT                              │
# └─────────────────────────────────────────────────────────────┘

class StudentFactory(factory.django.DjangoModelFactory):
    """
    Crée des Student avec des données réalistes pour les tests.
    
    Exemple:
    ────────
    student1 = StudentFactory()
    # Résultat: Student(id=1, first_name="Alice", last_name="Dupont", ...)
    
    student2 = StudentFactory(first_name="Jean")
    # Résultat: Student(id=2, first_name="Jean", last_name="Martin", ...)
    """
    
    # 1. Dire à Factory Boy quel modèle créer
    class Meta:
        model = Student  # ← Le modèle Django
    
    # 2. Définir les champs avec leurs valeurs
    
    # first_name: Générer un prénom aléatoire avec Faker
    first_name = factory.Faker('first_name')
    # Résultat: "Alice", "Bob", "Charlie", ... (aléatoire à chaque fois)
    
    # last_name: Générer un nom aléatoire avec Faker
    last_name = factory.Faker('last_name')
    # Résultat: "Dupont", "Martin", "Bernard", ... (aléatoire)
    
    # level: Valeur fixe (toujours L1)
    level = Student.LEVEL_L1  # ← Valeur par défaut
    # Résultat: toujours "L1" sauf override
    
    # email: Générer un email UNIQUE avec Sequence
    email = factory.Sequence(lambda n: f"student{n}@example.com")
    # Résultat: "student0@example.com", "student1@example.com", ...
    # ← Chaque Student a un email différent (numéroté)


# ┌─────────────────────────────────────────────────────────────┐
# │ FACTORY POUR LE MODÈLE SUBJECT                              │
# └─────────────────────────────────────────────────────────────┘

class SubjectFactory(factory.django.DjangoModelFactory):
    """Crée des Subject avec code unique et coefficient."""
    
    class Meta:
        model = Subject
    
    # code: Code UNIQUE (MAT000, MAT001, ...)
    code = factory.Sequence(lambda n: f"MAT{n:03d}")
    # Résultat: "MAT000", "MAT001", "MAT002", ...
    # ← Assurez que chaque code est unique
    
    # name: Nom aléatoire (Python, Math, ...)
    name = factory.Faker('word')
    # Résultat: "Python", "Mathematics", ...
    
    # coefficient: Valeur par défaut pour l'importance
    coefficient = 1.0
    # Résultat: toujours 1.0 sauf override


# ┌─────────────────────────────────────────────────────────────┐
# │ FACTORY POUR LE MODÈLE GRADE                                │
# └─────────────────────────────────────────────────────────────┘

class GradeFactory(factory.django.DjangoModelFactory):
    """Crée des Grade avec Student et Subject liés automatiquement."""
    
    class Meta:
        model = Grade
    
    # student: Créer automatiquement un Student!
    student = factory.SubFactory(StudentFactory)
    # ← Quand on crée une Grade, un Student est créé automatiquement
    # Résultat: Grade.student = Student(id=X, ...)
    
    # subject: Créer automatiquement un Subject!
    subject = factory.SubFactory(SubjectFactory)
    # ← Quand on crée une Grade, un Subject est créé automatiquement
    # Résultat: Grade.subject = Subject(id=Y, ...)
    
    # value: La note (valeur par défaut)
    value = 10.0
    # Résultat: toujours 10.0 sauf override
    
    # date: La date actuelle au moment de la création
    date = factory.LazyFunction(timezone.now)
    # ← Exécuté à chaque création pour avoir la vraie date
    # Résultat: 2026-02-05 (aujourd'hui)
    
    # comment: Commentaire vide par défaut
    comment = ''


# ┌─────────────────────────────────────────────────────────────┐
# │ EXEMPLES D'UTILISATION                                      │
# └─────────────────────────────────────────────────────────────┘

# Créer UN Student avec les valeurs par défaut
student = StudentFactory()
# Résultat:
# Student(
#   id=1,
#   first_name="Alice",      ← Aléatoire
#   last_name="Dupont",      ← Aléatoire
#   level="L1",              ← Par défaut
#   email="student0@example.com"  ← Unique (séquence)
# )

# Créer UN Student et OVERRIDE le prénom
student = StudentFactory(first_name="Jean")
# Résultat:
# Student(
#   id=2,
#   first_name="Jean",       ← Overridé (pas aléatoire)
#   last_name="Martin",      ← Aléatoire
#   level="L1",              ← Par défaut
#   email="student1@example.com"  ← Unique
# )

# Créer PLUSIEURS Students d'un coup
students = StudentFactory.create_batch(5)
# Résultat: 5 Students différents créés
# [Student(id=1, ...), Student(id=2, ...), ..., Student(id=5, ...)]

# Créer une Grade avec Student et Subject auto-créés
grade = GradeFactory()
# Résultat:
# Grade(
#   id=1,
#   student=Student(id=X, ...),    ← Créé automatiquement!
#   subject=Subject(id=Y, ...),    ← Créé automatiquement!
#   value=10.0,
#   date=2026-02-05,
#   comment=""
# )

# Créer une Grade avec Student spécifique
student = StudentFactory()
grade = GradeFactory(student=student)
# Résultat:
# Grade(
#   id=2,
#   student=student,               ← Réutilisé
#   subject=Subject(id=Z, ...),    ← Créé automatiquement
#   value=10.0,
#   date=2026-02-05
# )
```

---

## Étape 2: Créer une Fixture

### Qu'est-ce qu'on va faire?
Créer des fixtures réutilisables pour les tests.

### Code complet commenté

```python
# Fichier: grades_app/tests/conftest.py

import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient
from grades_app.tests.factories import GradeFactory, StudentFactory, SubjectFactory


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE SIMPLE: STUDENT                                     │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def student():
    """
    Crée un Student pour les tests.
    
    Utilisation:
    ────────────
    def test_something(student):  # student injecté automatiquement
        assert student.id is not None
    
    Scope: function (créé pour chaque test)
    """
    return StudentFactory()


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE SIMPLE: SUBJECT                                     │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def subject():
    """Crée un Subject pour les tests."""
    return SubjectFactory()


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE AVEC DÉPENDANCES: GRADE                             │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def grade(student, subject):
    """
    Crée une Grade avec Student et Subject liés.
    
    Dépendances:
    ────────────
    - student: la fixture student (créée automatiquement)
    - subject: la fixture subject (créée automatiquement)
    
    Flux:
    ──────
    1. pytest voit test_something(grade)
    2. pytest voit que grade dépend de student et subject
    3. pytest appelle StudentFactory() → student
    4. pytest appelle SubjectFactory() → subject
    5. pytest appelle GradeFactory(student=student, subject=subject) → grade
    6. pytest appelle test_something(grade)
    
    Utilisation:
    ────────────
    def test_grade(grade):
        # grade.student existe ✅
        # grade.subject existe ✅
        assert grade.value == 10.0
    """
    return GradeFactory(student=student, subject=subject)


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE: USER ADMIN                                         │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def admin_user(db):
    """
    Crée un User admin pour les tests.
    
    Paramètre db:
    ──────────────
    - 'db' = fixture intégrée de pytest-django
    - Permet d'accéder à la base de données
    - Remplace @pytest.mark.django_db
    
    Utilisation:
    ────────────
    def test_admin_access(admin_user):
        assert admin_user.is_superuser == True
        assert admin_user.username == 'admin'
    """
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='pass'
    )


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE: USER TEACHER                                       │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def teacher_user(db):
    """
    Crée un User enseignant avec le groupe 'enseignant'.
    
    Explications:
    ──────────────
    1. Créer un User normal (pas superuser)
    2. Créer ou récupérer le Group 'enseignant'
    3. Ajouter l'user au groupe
    
    Utilisation:
    ────────────
    def test_teacher_permissions(teacher_user):
        assert teacher_user.groups.filter(name='enseignant').exists()
    """
    user = User.objects.create_user(
        username='teacher',
        email='teacher@example.com',
        password='pass'
    )
    group, _ = Group.objects.get_or_create(name='enseignant')
    user.groups.add(group)
    return user


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE: USER ÉTUDIANT                                      │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def student_user(db):
    """Crée un User étudiant avec le groupe 'etudiant'."""
    user = User.objects.create_user(
        username='student',
        email='student@example.com',
        password='pass'
    )
    group, _ = Group.objects.get_or_create(name='etudiant')
    user.groups.add(group)
    return user


# ┌─────────────────────────────────────────────────────────────┐
# │ FIXTURE: API CLIENT AUTHENTIFIÉ                             │
# └─────────────────────────────────────────────────────────────┘

@pytest.fixture
def authenticated_client(db, admin_user):
    """
    Crée un APIClient authentifié en tant qu'admin.
    
    Dépendances:
    ────────────
    - db: accès à la base de données
    - admin_user: l'admin créé par la fixture admin_user
    
    Explications:
    ──────────────
    1. Créer un APIClient (client HTTP pour Django REST)
    2. Authentifier le client avec l'admin_user
    3. Retourner le client prêt à faire des requêtes
    
    Utilisation:
    ────────────
    def test_api_endpoint(authenticated_client):
        response = authenticated_client.get('/api/students/')
        assert response.status_code == 200
    """
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
```

---

## Étape 3: Écrire un test unitaire

### Qu'est-ce qu'on va faire?
Écrire un test simple qui vérifie qu'un Student peut être créé.

### Code complet commenté

```python
# Fichier: grades_app/tests/unit/test_models.py

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from grades_app.models import Student
from grades_app.tests.factories import StudentFactory


# ┌─────────────────────────────────────────────────────────────┐
# │ CLASSE DE TEST - GROUPER LES TESTS LIÉS                     │
# └─────────────────────────────────────────────────────────────┘

class TestStudentModel:
    """Tests pour le modèle Student."""
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 1: CRÉATION SIMPLE                               │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_student_creation_with_required_fields(self):
        """
        Test de création d'un Student.
        
        Nom du test:
        ────────────
        test_student_creation_with_required_fields
        ↑ Commence par 'test_'
        ↑ Décrit clairement ce qu'on teste
        
        Docstring:
        ──────────
        "Test de création d'un Student."
        ↑ Explique le but du test
        
        Marqueur:
        ─────────
        @pytest.mark.django_db
        ↑ Indique que ce test accède à la BD
        
        Corps:
        ──────
        """
        
        # ARRANGE - Préparer les données
        # Créer un Student avec des valeurs spécifiques
        student = StudentFactory(
            first_name="Alice",
            last_name="Dupont",
            email="alice@example.com"
        )
        # Résultat:
        # Student(
        #   id=None (pas encore en BD),
        #   first_name="Alice",
        #   last_name="Dupont",
        #   email="alice@example.com"
        # )
        
        # ACT - Exécuter l'action
        # StudentFactory appelle Student.objects.create()
        # Ce qui exécute Student.save()
        # Ce qui affecte l'ID et autre
        
        # ASSERT - Vérifier le résultat
        assert student.id is not None
        # ↑ L'ID a été affecté (il existe en BD)
        
        assert student.first_name == "Alice"
        # ↑ Le prénom est correct
        
        assert student.last_name == "Dupont"
        # ↑ Le nom est correct
        
        assert student.email == "alice@example.com"
        # ↑ L'email est correct
    
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 2: VÉRIFIER UNE CONTRAINTE UNIQUE                │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_student_email_must_be_unique(self):
        """
        Test que l'email ne peut pas être dupliqué.
        
        Objectif:
        ─────────
        Vérifier qu'on ne peut pas créer 2 Students avec le même email
        
        Méthode:
        ────────
        1. Créer un Student avec email 'unique@example.com'
        2. Essayer de créer un autre Student avec le même email
        3. Vérifier qu'une IntegrityError est levée
        """
        
        # ARRANGE - Créer le premier Student
        StudentFactory(email='unique@example.com')
        # Cet étudiant est sauvegardé en BD
        
        # ACT & ASSERT - Essayer de créer un doublon
        # On combine ACT et ASSERT car c'est une exception
        with pytest.raises(IntegrityError):
            # ↑ "Je m'attends à une IntegrityError"
            
            # Essayer de créer un second Student avec le même email
            StudentFactory(email='unique@example.com')
            # ↑ Cela va déclencher IntegrityError (contrainte UNIQUE)
        
        # Si aucune IntegrityError n'est levée → test échoue ❌
        # Si IntegrityError est levée → test passe ✅
    
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 3: VÉRIFIER L'AUTO-GÉNÉRATION                    │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_student_auto_generates_matricule(self):
        """
        Test que le matricule est généré automatiquement.
        
        Explications:
        ──────────────
        Quand on crée un Student sans fournir de matricule,
        le Student.save() appelle generate_matricule()
        qui génère automatiquement un matricule YYYYNNNN
        """
        
        # ARRANGE - Créer un Student (sans matricule!)
        student = StudentFactory()
        # StudentFactory n'a pas matricule=...
        # Donc le Student.save() génère matricule automatiquement
        
        # ASSERT - Vérifier que matricule est créé
        assert student.matricule is not None
        # ↑ Le matricule existe
        
        assert len(student.matricule) == 8
        # ↑ Le format est YYYYNNNN (8 caractères)
        
        from django.utils import timezone
        year = timezone.now().year
        assert student.matricule.startswith(str(year))
        # ↑ Commence par l'année actuelle (2026)
```

---

## Étape 4: Écrire un test d'intégration

### Qu'est-ce qu'on va faire?
Écrire un test qui teste le workflow complet via l'API.

### Code complet commenté

```python
# Fichier: grades_app/tests/integration/test_api_flow.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from grades_app.models import Student, Subject
from grades_app.tests.factories import StudentFactory


class TestStudentAPI:
    """Tests de l'API Students."""
    
    # ┌───────────────────────────────────────────────────────┐
    # │ FIXTURE LOCALE: CLIENT API                            │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.fixture
    def client(self):
        """
        Crée un APIClient authentifié pour les tests.
        
        Scope: class (partagé par tous les tests de la classe)
        """
        client = APIClient()
        # Créer un admin
        admin = User.objects.create_superuser(
            'admin',
            'admin@example.com',
            'pass'
        )
        # Authentifier le client
        client.force_authenticate(user=admin)
        return client
    
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 1: LISTER LES ÉTUDIANTS                          │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_list_students(self, client):
        """
        Test du endpoint GET /api/students/
        
        Utilisation:
        ────────────
        GET /api/students/
        Résultat: Lister tous les Students
        """
        
        # ARRANGE - Créer 3 Students en BD
        StudentFactory.create_batch(3)
        # ↑ Crée 3 Students différents
        
        # ACT - Faire une requête GET à l'API
        response = client.get('/api/students/')
        # ↑ Appel HTTP GET au endpoint
        
        # ASSERT - Vérifier le résultat
        assert response.status_code == 200
        # ↑ La requête a réussi (200 OK)
        
        assert len(response.data) == 3
        # ↑ On a reçu 3 Students
    
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 2: CRÉER UN STUDENT VIA API                      │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_create_student(self, client):
        """
        Test du endpoint POST /api/students/
        
        Utilisation:
        ────────────
        POST /api/students/
        Body: {first_name, last_name, level, email}
        Résultat: Créer un Student et retourner ses données
        """
        
        # ARRANGE - Préparer les données à envoyer
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'level': 'L1',
            'email': 'john@example.com'
        }
        # ↑ JSON que nous envoyons à l'API
        
        # ACT - Faire une requête POST à l'API
        response = client.post('/api/students/', data)
        # ↑ Envoyer les données et créer le Student
        
        # ASSERT - Vérifier le résultat
        assert response.status_code == 201
        # ↑ Créé avec succès (201 Created)
        
        assert response.data['first_name'] == 'John'
        # ↑ Les données renvoyées sont correctes
        
        assert 'matricule' in response.data
        # ↑ Le matricule est inclus dans la réponse
        
        # Vérifier en BD que l'étudiant a été créé
        student = Student.objects.get(email='john@example.com')
        assert student.first_name == 'John'
        # ↑ L'étudiant existe vraiment en BD
    
    
    # ┌───────────────────────────────────────────────────────┐
    # │ TEST 3: WORKFLOW COMPLET                              │
    # └───────────────────────────────────────────────────────┘
    
    @pytest.mark.django_db
    def test_complete_workflow_create_student_and_add_grades(self, client):
        """
        Test du workflow complet:
        1. Créer un Student
        2. Créer des Subjects
        3. Ajouter des Grades
        4. Vérifier la moyenne
        
        Objectif:
        ──────────
        Tester que tout fonctionne ensemble
        """
        
        # ════════════════════════════════════════════════════
        # ÉTAPE 1: CRÉER UN STUDENT VIA API
        # ════════════════════════════════════════════════════
        
        student_data = {
            'first_name': 'Alice',
            'last_name': 'Dupont',
            'level': 'L1',
            'email': 'alice@example.com'
        }
        response = client.post('/api/students/', student_data)
        assert response.status_code == 201
        student_id = response.data['id']  # Récupérer l'ID
        matricule = response.data['matricule']  # Récupérer le matricule généré
        
        # Vérifications
        assert student_id is not None
        assert len(matricule) == 8  # Format YYYYNNNN
        
        # ════════════════════════════════════════════════════
        # ÉTAPE 2: CRÉER DES SUBJECTS VIA API
        # ════════════════════════════════════════════════════
        
        math_data = {
            'code': 'MATH',
            'name': 'Mathématiques',
            'coefficient': 2.0
        }
        response = client.post('/api/subjects/', math_data)
        assert response.status_code == 201
        math_id = response.data['id']
        
        physics_data = {
            'code': 'PHYS',
            'name': 'Physique',
            'coefficient': 1.0
        }
        response = client.post('/api/subjects/', physics_data)
        assert response.status_code == 201
        physics_id = response.data['id']
        
        # ════════════════════════════════════════════════════
        # ÉTAPE 3: AJOUTER DES GRADES VIA API
        # ════════════════════════════════════════════════════
        
        # Grade 1: Math 16.0
        grade1_data = {
            'student': student_id,
            'subject': math_id,
            'value': 16.0
        }
        response = client.post('/api/grades/', grade1_data)
        assert response.status_code == 201
        
        # Grade 2: Physique 12.0
        grade2_data = {
            'student': student_id,
            'subject': physics_id,
            'value': 12.0
        }
        response = client.post('/api/grades/', grade2_data)
        assert response.status_code == 201
        
        # ════════════════════════════════════════════════════
        # ÉTAPE 4: VÉRIFIER LA MOYENNE
        # ════════════════════════════════════════════════════
        
        response = client.get(f'/api/students/{student_id}/average/')
        assert response.status_code == 200
        
        # Calcul: (16×2 + 12×1) / (2+1) = 44/3 = 14.67
        expected_average = 14.67
        assert response.data['average'] == expected_average
        
        # ════════════════════════════════════════════════════
        # RÉSULTAT: TOUT FONCTIONNE ENSEMBLE ✅
        # ════════════════════════════════════════════════════
```

---

## Étape 5: Utiliser les assertions

### Code complet commenté

```python
# Différents types d'assertions et comment les utiliser

class TestAssertions:
    """Exemples de différentes assertions."""
    
    @pytest.mark.django_db
    def test_various_assertions(self):
        """Démontrer différents types d'assertions."""
        
        # 1. ÉGALITÉ
        # ─────────
        value = 10
        assert value == 10      # ✅ PASSE
        assert value != 5       # ✅ PASSE
        assert value == 5       # ❌ ÉCHOUE
        
        # 2. COMPARAISON
        # ──────────────
        age = 25
        assert age > 18         # ✅ PASSE
        assert age <= 25        # ✅ PASSE
        assert age < 18         # ❌ ÉCHOUE
        
        # 3. EXISTENCE
        # ────────────
        student = StudentFactory()
        assert student.id is not None           # ✅ PASSE (ID existe)
        assert student.first_name is not None   # ✅ PASSE
        
        # 4. MEMBERSHIP (dans une liste)
        # ──────────────────────────────
        level = Student.LEVEL_L1
        levels = [Student.LEVEL_L1, Student.LEVEL_L2]
        assert level in levels      # ✅ PASSE
        assert 'L3' in ['L1', 'L2', 'L3']  # ✅ PASSE
        
        # 5. CHAÎNES
        # ──────────
        name = "Alice Dupont"
        assert "Alice" in name      # ✅ PASSE
        assert name.startswith("Alice")  # ✅ PASSE
        
        # 6. LONGUEUR
        # ───────────
        students = StudentFactory.create_batch(3)
        assert len(students) == 3   # ✅ PASSE
        assert len(students) != 5   # ✅ PASSE
        
        # 7. CONTENU D'UNE LISTE
        # ──────────────────────
        values = [10, 20, 30]
        assert 20 in values         # ✅ PASSE
        assert 50 not in values     # ✅ PASSE
        
        # 8. REGEX (expression régulière)
        # ─────────────────────────────
        import re
        student = StudentFactory()
        # Le matricule doit être YYYYNNNN
        assert re.match(r'^\d{8}$', student.matricule)  # ✅ PASSE
```

---

## Étape 6: Tester les exceptions

### Code complet commenté

```python
# Comment tester que les exceptions sont levées correctement

class TestExceptions:
    """Tests des exceptions levées."""
    
    @pytest.mark.django_db
    def test_grade_validation_exceptions(self):
        """Tester que les validations lèvent les bonnes exceptions."""
        
        student = StudentFactory()
        subject = SubjectFactory()
        
        # ┌───────────────────────────────────────────────┐
        # │ TEST 1: NOTE NÉGATIVE (INVALIDE)              │
        # └───────────────────────────────────────────────┘
        
        with pytest.raises(ValidationError):
            # ↑ "Je m'attends à une ValidationError"
            
            # Créer une Grade avec une note négative
            grade = Grade(student=student, subject=subject, value=-5)
            grade.full_clean()  # Déclenche la validation
            
            # Flux:
            # 1. Grade(value=-5) créé (pas de validation ici)
            # 2. full_clean() est appelé
            # 3. clean() method est appelée
            # 4. validate_grade(-5) est appelé
            # 5. ValidationError levée ✅
            # 6. pytest.raises l'attrape ✅
            # 7. Test passe ✅
        
        # ┌───────────────────────────────────────────────┐
        # │ TEST 2: NOTE > 20 (INVALIDE)                  │
        # └───────────────────────────────────────────────┘
        
        with pytest.raises(ValidationError):
            # Créer une Grade avec une note > 20
            grade = Grade(student=student, subject=subject, value=25)
            grade.full_clean()
            # ValidationError levée ✅
        
        # ┌───────────────────────────────────────────────┐
        # │ TEST 3: NOTE VALIDE (10.0)                    │
        # └───────────────────────────────────────────────┘
        
        # CAS SANS EXCEPTION
        grade = Grade(student=student, subject=subject, value=10.0)
        grade.full_clean()  # Pas d'exception
        grade.save()
        assert grade.id is not None  # ✅ Créé avec succès
        
        # ┌───────────────────────────────────────────────┐
        # │ TEST 4: EXCEPTION SPÉCIFIQUE                  │
        # └───────────────────────────────────────────────┘
        
        # Vérifier qu'on lève la BONNE exception
        with pytest.raises(ValidationError) as exc_info:
            grade = Grade(student=student, subject=subject, value=25)
            grade.full_clean()
        
        # Vérifier le message d'erreur
        assert 'Grade must be between 0 and 20' in str(exc_info.value)
        # ↑ La validation lève le bon message ✅
        
        # ┌───────────────────────────────────────────────┐
        # │ TEST 5: MAUVAISE EXCEPTION (ÉCHOUE)           │
        # └───────────────────────────────────────────────┘
        
        # Cette assertion va ÉCHOUER car:
        # - On attend une ValidationError
        # - Mais aucune exception n'est levée
        
        # with pytest.raises(ValidationError):
        #     grade = Grade(student=student, subject=subject, value=15.0)
        #     grade.full_clean()  # Pas d'exception!
        # ↑ Test échouerait: "DID NOT RAISE ValidationError"
```

---

## Code Complet

### Fichier 1: factories.py

```python
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
```

### Fichier 2: conftest.py

```python
import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient
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
def authenticated_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
```

### Fichier 3: Exécuter les tests

```bash
# Tous les tests
pytest grades_app/tests/ -v

# Avec couverture
pytest grades_app/tests/ --cov=grades_app --cov-report=term-missing

# Un fichier spécifique
pytest grades_app/tests/unit/test_models.py -v

# Une classe spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel -v

# Un test spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel::test_student_creation_with_required_fields -v
```

