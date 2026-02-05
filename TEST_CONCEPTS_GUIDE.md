# 📚 Guide Complet des Concepts de Test

## Table des Matières
1. [Vue d'ensemble](#vue-densemble)
2. [pytest - Le framework de test](#pytest)
3. [Factory Boy - Création de données](#factory-boy)
4. [Fixtures - Réutiliser les données](#fixtures)
5. [Marqueurs pytest](#marqueurs)
6. [Tests Unitaires vs Intégration](#tests-unitaires-vs-intégration)
7. [Patterns et meilleures pratiques](#patterns)
8. [Exemples concrets](#exemples-concrets)

---

## Vue d'ensemble

Un test vérifie qu'une partie du code fonctionne comme prévu. En Python Django, nous utilisons 3 outils principaux:

| Outil | Rôle | Exemple |
|-------|------|---------|
| **pytest** | Framework d'exécution | `@pytest.mark.django_db` |
| **factory-boy** | Créer des données de test | `StudentFactory()` |
| **Fixtures** | Partager des données entre tests | `@pytest.fixture` |

### Structure des tests
```
tests/
├── conftest.py          # Fixtures partagées
├── factories.py         # Création de données
├── unit/                # Tests isolés
│   ├── test_models.py   # Tests des modèles
│   └── test_services.py # Tests des services
└── integration/
    └── test_api_flow.py # Tests des workflows complets
```

---

## pytest

### Qu'est-ce que pytest?

**pytest** est un framework qui exécute vos tests et rapporte les résultats. C'est l'outil que vous utilisiez quand vous faisiez:

```bash
pytest grades_app/tests/ -v
```

### Les éléments clés de pytest

#### 1. Une fonction de test

```python
# ✅ BON
def test_student_creation_with_required_fields():
    """Les tests commencent par 'test_'."""
    student = StudentFactory(
        first_name="Alice",
        last_name="Dupont"
    )
    assert student.first_name == "Alice"  # Vérification
    assert student.last_name == "Dupont"  # Vérification

# ❌ MAUVAIS - ne sera pas exécuté
def check_student_creation():
    pass
```

**Règles:**
- Le nom doit commencer par `test_`
- Le nom décrit ce qu'on teste
- On utilise `assert` pour vérifier (pas `print()`)

#### 2. Les assertions (vérifications)

```python
# Vérifier l'égalité
assert student.first_name == "Alice"

# Vérifier qu'une condition est vraie
assert student.id is not None

# Vérifier qu'une condition est fausse
assert student.email not in "invalid@"

# Vérifier qu'une exception est levée
with pytest.raises(ValidationError):
    grade = Grade(value=25)  # Invalide (max 20)
    grade.full_clean()

# Vérifier qu'une liste a un nombre d'éléments
assert len(students) == 3

# Vérifier qu'une valeur est dans une liste
assert student.level in ['L1', 'L2', 'L3']
```

#### 3. Les classes de test

Grouper les tests par thème:

```python
class TestStudentModel:
    """Tous les tests du modèle Student."""
    
    @pytest.mark.django_db
    def test_student_creation(self):
        student = StudentFactory()
        assert student.id is not None
    
    @pytest.mark.django_db
    def test_student_email_unique(self):
        StudentFactory(email='same@example.com')
        with pytest.raises(IntegrityError):
            StudentFactory(email='same@example.com')

class TestSubjectModel:
    """Tous les tests du modèle Subject."""
    
    @pytest.mark.django_db
    def test_subject_creation(self):
        subject = SubjectFactory()
        assert subject.id is not None
```

**Avantages:**
- Code mieux organisé
- Plus facile à naviguer
- Chaque classe a sa responsabilité

#### 4. Docstrings clairs

```python
@pytest.mark.django_db
def test_student_auto_generates_matricule(self):
    """Le matricule est généré automatiquement au save."""
    # La docstring explique QUOI on teste
    
    student = StudentFactory()
    assert student.matricule is not None
    assert len(student.matricule) == 8
```

---

## Factory Boy

### Qu'est-ce que Factory Boy?

C'est une bibliothèque pour **créer rapidement des données de test** sans taper les détails à chaque fois.

### Sans Factory Boy ❌

```python
def test_student_creation():
    student = Student.objects.create(
        first_name="Alice",
        last_name="Dupont",
        email="alice@example.com",
        level="L1"
    )
    assert student.id is not None
```

Problèmes:
- Beaucoup de code répétitif
- Si on ajoute un champ obligatoire, tous les tests cassent
- Difficile à maintenir

### Avec Factory Boy ✅

```python
def test_student_creation():
    student = StudentFactory()
    assert student.id is not None
```

Beaucoup plus simple!

### Créer une Factory

Fichier: `factories.py`

```python
import factory
from django.utils import timezone
from grades_app.models import Student, Subject, Grade

class StudentFactory(factory.django.DjangoModelFactory):
    """Factory pour créer des Students."""
    
    class Meta:
        model = Student  # Le modèle à créer
    
    # Les champs avec leurs valeurs par défaut
    first_name = factory.Faker('first_name')  # Nom aléatoire
    last_name = factory.Faker('last_name')    # Prénom aléatoire
    level = Student.LEVEL_L1                   # Niveau par défaut
    email = factory.Sequence(lambda n: f"student{n}@example.com")  # Email unique
```

**Concepts clés:**

| Concept | Exemple | Résultat |
|---------|---------|----------|
| **Valeur fixe** | `level = Student.LEVEL_L1` | Tous les tests: L1 |
| **Faker aléatoire** | `first_name = factory.Faker('first_name')` | Alice, Bob, Charlie... |
| **Sequence unique** | `email = factory.Sequence(lambda n: f"student{n}@example.com")` | student0@, student1@, student2@... |
| **SubFactory** | `student = factory.SubFactory(StudentFactory)` | Crée automatiquement un Student associé |

### Utiliser une Factory

```python
# Créer UN objet
student = StudentFactory()
student = StudentFactory(first_name="Alice")  # Overrider des champs

# Créer PLUSIEURS objets
students = StudentFactory.create_batch(5)  # 5 students avec données aléatoires

# Créer juste la structure (pas de sauvegarde BD)
student_dict = StudentFactory.build()
```

### Example complet avec Factory Boy

```python
class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
    
    code = factory.Sequence(lambda n: f"MAT{n:03d}")  # MAT000, MAT001...
    name = factory.Faker('word')                       # "Python", "Math"...
    coefficient = 1.0                                  # Par défaut 1.0

class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Grade
    
    # Crée automatiquement un Student et Subject
    student = factory.SubFactory(StudentFactory)
    subject = factory.SubFactory(SubjectFactory)
    value = 10.0                                # Note 10/20
    date = factory.LazyFunction(timezone.now)  # Date actuelle
    comment = ''

# Usage:
grade = GradeFactory()  # Grade complet avec Student et Subject auto-créés!
grade.student.first_name  # 'Alice' (généré)
grade.subject.code        # 'MAT000' (généré)
grade.value              # 10.0
```

---

## Fixtures

### Qu'est-ce qu'une Fixture?

Une **fixture** est une fonction réutilisable qui crée des données pour vos tests. C'est comme un "setup" automatique.

### Sans Fixture ❌

```python
def test_student_email_unique_1():
    student1 = StudentFactory(email='unique@example.com')
    with pytest.raises(IntegrityError):
        StudentFactory(email='unique@example.com')

def test_student_email_unique_2():
    student1 = StudentFactory(email='unique@example.com')
    with pytest.raises(IntegrityError):
        StudentFactory(email='unique@example.com')

# Même code répété 10 fois... 🤮
```

### Avec Fixture ✅

Fichier: `conftest.py`

```python
import pytest
from grades_app.tests.factories import StudentFactory

@pytest.fixture
def student():
    """Fixture qui crée un Student."""
    return StudentFactory()

@pytest.fixture
def admin_user(db):
    """Fixture qui crée un User admin."""
    return User.objects.create_superuser('admin', 'admin@example.com', 'pass')
```

Utilisation dans les tests:

```python
def test_something(student):  # Injection de la fixture!
    """Cette fonction reçoit automatiquement un Student."""
    assert student.id is not None

def test_admin_access(admin_user):
    """Cette fonction reçoit automatiquement un admin."""
    assert admin_user.is_superuser
```

**Avantages:**
- Code réutilisable
- Facile à modifier (une seule place à changer)
- Noms expressifs (auto-documentés)

### Fixtures avec dépendances

```python
@pytest.fixture
def student():
    return StudentFactory()

@pytest.fixture
def subject():
    return SubjectFactory()

@pytest.fixture
def grade(student, subject):  # Dépend des deux autres!
    """Crée une Grade avec un Student et Subject."""
    return GradeFactory(student=student, subject=subject)

# Usage:
def test_grade_value(grade):  # Reçoit grade + student + subject auto!
    assert grade.value == 10.0
    assert grade.student.id is not None
    assert grade.subject.id is not None
```

### Paramètres des Fixtures

```python
@pytest.fixture
def authenticated_client():
    """APIClient authentifié."""
    client = APIClient()
    user = User.objects.create_user('test', 'test@example.com', 'pass')
    client.force_authenticate(user=user)
    return client

def test_api_endpoint(authenticated_client):
    response = authenticated_client.get('/api/students/')
    assert response.status_code == 200
```

### Scopes de Fixtures

```python
# @pytest.fixture()  - Par défaut: "function" (exécuté à chaque test)
# Crée une nouvelle instance à chaque test

@pytest.fixture(scope="class")  # Partagée par une classe
def student():
    return StudentFactory()

@pytest.fixture(scope="module")  # Partagée par tout un fichier
def admin_user(db):
    return User.objects.create_superuser('admin', 'admin@example.com', 'pass')

@pytest.fixture(scope="session")  # Partagée pour toute la session de test
def database_setup():
    # Configuration longue
    pass
```

---

## Marqueurs pytest

### Qu'est-ce que c'est?

Les marqueurs sont des annotations qui donnent des **instructions spéciales** à pytest.

### @pytest.mark.django_db

**C'est le plus important!**

```python
@pytest.mark.django_db
def test_student_creation():
    """Ce test accède à la base de données."""
    student = StudentFactory()  # Crée dans la BD
    assert student.id is not None
```

**Pourquoi c'est nécessaire?**
- Les tests de Django doivent isoler la BD
- Sans ce marqueur, pytest lève une erreur
- Cela crée une BD de test à chaque test

```python
# ❌ ERREUR
def test_student_creation():
    student = StudentFactory()  # RuntimeError!

# ✅ BON
@pytest.mark.django_db
def test_student_creation():
    student = StudentFactory()  # OK!
```

### Autres marqueurs utiles

```python
@pytest.mark.django_db(transaction=True)
def test_with_transactions():
    """Test avec transactions réelles (plus lent)."""
    pass

@pytest.mark.skipif(condition, reason="Pourquoi on skip")
def test_skipped_sometimes():
    """Ce test sera passé si condition est vraie."""
    pass

@pytest.mark.skip(reason="Pas encore implémenté")
def test_not_implemented():
    """Ce test est toujours ignoré."""
    pass

@pytest.mark.xfail
def test_expected_failure():
    """Ce test DOIT échouer."""
    pass
```

---

## Tests Unitaires vs Intégration

### Tests Unitaires

**Définition:** Tester UNE partie du code isolée.

```python
# test_models.py - Tests unitaires

@pytest.mark.django_db
def test_student_creation_with_required_fields():
    """Test ISOLÉ du modèle Student."""
    student = StudentFactory(
        first_name="Alice",
        last_name="Dupont"
    )
    # On teste JUSTE le modèle
    # Pas l'API, pas la base de données, juste Student
    assert student.first_name == "Alice"

@pytest.mark.django_db
def test_student_email_must_be_unique():
    """Test de la contrainte unique de email."""
    StudentFactory(email='unique@example.com')
    with pytest.raises(IntegrityError):
        StudentFactory(email='unique@example.com')
```

**Caractéristiques:**
- ✅ Rapide (< 1ms chacun)
- ✅ Isolé (ne teste qu'une chose)
- ✅ Facile à déboguer
- ❌ Ne teste pas les interactions

### Tests d'Intégration

**Définition:** Tester PLUSIEURS parties ensemble.

```python
# test_api_flow.py - Tests d'intégration

@pytest.mark.django_db
def test_create_student_and_get_average(client):
    """Workflow complet: créer étudiant → ajouter notes → calculer moyenne."""
    
    # 1. Créer un étudiant via API
    data = {
        'first_name': 'Alice',
        'last_name': 'Dupont',
        'level': 'L1',
        'email': 'alice@example.com'
    }
    response = client.post('/api/students/', data)
    assert response.status_code == 201
    student_id = response.data['id']
    
    # 2. Créer des matières
    response = client.post('/api/subjects/', {
        'code': 'MAT001',
        'name': 'Math',
        'coefficient': 2.0
    })
    subject_id = response.data['id']
    
    # 3. Ajouter une note
    response = client.post('/api/grades/', {
        'student': student_id,
        'subject': subject_id,
        'value': 15.5
    })
    assert response.status_code == 201
    
    # 4. Vérifier la moyenne calculée
    response = client.get(f'/api/students/{student_id}/average/')
    assert response.data['average'] == 15.5
```

**Caractéristiques:**
- ✅ Teste les vraies interactions
- ✅ Trouve les bugs entre composants
- ❌ Lent (plusieurs opérations)
- ❌ Plus difficile à déboguer

### Comparaison

| Aspect | Unitaire | Intégration |
|--------|----------|-------------|
| **Périmètre** | Une classe/fonction | Plusieurs composants |
| **Vitesse** | Très rapide | Plus lent |
| **Maintenance** | Facile | Difficile |
| **Détection** | Bugs localisés | Bugs d'interaction |
| **Exemple** | test_models.py | test_api_flow.py |

---

## Patterns et Meilleures Pratiques

### 1. Pattern AAA (Arrange-Act-Assert)

Toujours organiser les tests de la même manière:

```python
@pytest.mark.django_db
def test_student_compute_general_average():
    """Vérifier le calcul de la moyenne générale."""
    
    # ARRANGE - Préparer les données
    student = StudentFactory()
    subject1 = SubjectFactory(coefficient=2.0)
    subject2 = SubjectFactory(coefficient=1.0)
    GradeFactory(student=student, subject=subject1, value=16.0)  # 16 × 2 = 32
    GradeFactory(student=student, subject=subject2, value=12.0)  # 12 × 1 = 12
    
    # ACT - Exécuter l'action
    average = student.compute_general_average()
    
    # ASSERT - Vérifier le résultat
    # (16×2 + 12×1) / (2+1) = 44/3 = 14.67
    assert average == 14.67
```

**Avantages:**
- Lisibilité claire
- Structure cohérente
- Facile à modifier

### 2. One assertion per test (idéalement)

```python
# ❌ Trop de vérifications différentes
@pytest.mark.django_db
def test_student():
    student = StudentFactory(first_name="Alice")
    assert student.first_name == "Alice"
    assert student.id is not None
    assert student.email is not None
    assert student.level == Student.LEVEL_L1
    # Si une échoue, on ne sait pas laquelle

# ✅ Chaque test une vérification
@pytest.mark.django_db
def test_student_first_name():
    student = StudentFactory(first_name="Alice")
    assert student.first_name == "Alice"

@pytest.mark.django_db
def test_student_has_id():
    student = StudentFactory()
    assert student.id is not None

@pytest.mark.django_db
def test_student_has_email():
    student = StudentFactory()
    assert student.email is not None
```

**Avantage:** Si un test échoue, on sait EXACTEMENT ce qui n'a pas fonctionné.

### 3. Noms descriptifs

```python
# ❌ Vague
def test_student():
    pass

# ✅ Très clair
def test_student_email_must_be_unique():
    """L'email ne peut pas être dupliqué."""
    StudentFactory(email='duplicate@example.com')
    with pytest.raises(IntegrityError):
        StudentFactory(email='duplicate@example.com')
```

Lire le nom du test devrait suffire à comprendre ce qu'il teste.

### 4. Isoler les tests (pas d'état partagé)

```python
# ❌ MAUVAIS - Dépendance entre tests
student_global = None

def test_create_student():
    global student_global
    student_global = StudentFactory()
    assert student_global.id is not None

def test_update_student():
    student_global.level = Student.LEVEL_L2  # Dépend du test précédent!
    student_global.save()
    assert student_global.level == Student.LEVEL_L2

# ✅ BON - Chaque test est indépendant
@pytest.mark.django_db
def test_create_student():
    student = StudentFactory()
    assert student.id is not None

@pytest.mark.django_db
def test_update_student():
    student = StudentFactory(level=Student.LEVEL_L1)
    student.level = Student.LEVEL_L2
    student.save()
    assert student.level == Student.LEVEL_L2
```

**Avantage:** On peut exécuter les tests dans n'importe quel ordre.

---

## Exemples Concrets

### Exemple 1: Tester la Validation d'une Note

```python
@pytest.mark.django_db
class TestGradeValidation:
    """Tests pour la validation des notes."""
    
    def test_grade_value_must_be_between_0_and_20(self):
        """Une note doit être entre 0 et 20."""
        # ARRANGE
        student = StudentFactory()
        subject = SubjectFactory()
        
        # ACT & ASSERT - Valeur basse
        with pytest.raises(ValidationError):
            grade = Grade(student=student, subject=subject, value=-1)
            grade.full_clean()  # Validation
        
        # ACT & ASSERT - Valeur haute
        with pytest.raises(ValidationError):
            grade = Grade(student=student, subject=subject, value=25)
            grade.full_clean()  # Validation
        
        # ACT & ASSERT - Valeur valide
        grade = Grade(student=student, subject=subject, value=15)
        grade.full_clean()  # Pas d'exception
        grade.save()
        assert grade.id is not None
    
    def test_grade_value_accepts_decimals(self):
        """Les notes peuvent avoir des décimales."""
        student = StudentFactory()
        subject = SubjectFactory()
        grade = Grade(student=student, subject=subject, value=15.5)
        grade.full_clean()
        grade.save()
        assert grade.value == 15.5
```

### Exemple 2: Tester la Génération de Matricule

```python
@pytest.mark.django_db
class TestMatriculeGeneration:
    """Tests pour la génération du matricule."""
    
    def test_matricule_format_is_yyyynnnn(self):
        """Format du matricule: YYYYNNNN."""
        student = StudentFactory()
        assert len(student.matricule) == 8
        assert student.matricule[:4].isdigit()  # Année
        assert student.matricule[4:].isdigit()  # Numéro
        assert student.matricule[:4] == str(timezone.now().year)
    
    def test_matricule_auto_increments(self):
        """Les matricules s'incrémentent."""
        year = timezone.now().year
        # Créer manuellement deux étudiants avec matricules séquentiels
        student1 = StudentFactory(matricule=f"{year}0001")
        student2 = StudentFactory(matricule=f"{year}0002")
        
        # Vérifier que le prochain généré ne duplique pas
        next_matricule = generate_matricule(year=year)
        assert next_matricule not in [student1.matricule, student2.matricule]
```

### Exemple 3: Tester le Calcul de Moyenne

```python
@pytest.mark.django_db
class TestAverageCalculation:
    """Tests pour le calcul de la moyenne."""
    
    def test_compute_general_average_with_coefficients(self):
        """La moyenne tient compte des coefficients."""
        # ARRANGE
        student = StudentFactory()
        math = SubjectFactory(code='MATH', coefficient=2.0)
        physics = SubjectFactory(code='PHYS', coefficient=1.0)
        
        # Math: 16, Physique: 12
        # Moyenne = (16×2 + 12×1) / (2+1) = 44/3 = 14.67
        GradeFactory(student=student, subject=math, value=16.0)
        GradeFactory(student=student, subject=physics, value=12.0)
        
        # ACT
        average = student.compute_general_average()
        
        # ASSERT
        assert average == round((16.0 * 2.0 + 12.0 * 1.0) / 3.0, 2)
    
    def test_student_with_no_grades_has_zero_average(self):
        """Un étudiant sans notes a une moyenne de 0."""
        student = StudentFactory()
        assert student.compute_general_average() == 0.0
```

### Exemple 4: Tester l'API REST

```python
@pytest.mark.django_db
class TestStudentAPI:
    """Tests pour l'API Students."""
    
    @pytest.fixture
    def authenticated_client(self):
        """Client API authentifié en admin."""
        client = APIClient()
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pass')
        client.force_authenticate(user=admin)
        return client
    
    def test_list_students(self, authenticated_client):
        """Lister les étudiants via API."""
        # ARRANGE
        StudentFactory.create_batch(3)
        
        # ACT
        response = authenticated_client.get('/api/students/')
        
        # ASSERT
        assert response.status_code == 200
        assert len(response.data) == 3
    
    def test_create_student_via_api(self, authenticated_client):
        """Créer un étudiant via API génère le matricule."""
        # ARRANGE
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'level': 'L1',
            'email': 'john@example.com'
        }
        
        # ACT
        response = authenticated_client.post('/api/students/', data)
        
        # ASSERT
        assert response.status_code == 201
        assert 'matricule' in response.data
        assert len(response.data['matricule']) == 8
        
        # Vérifier en BD
        student = Student.objects.get(email='john@example.com')
        assert student.matricule == response.data['matricule']
```

---

## Résumé Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                         PYRAMIDE DE TEST                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ▲  Tests E2E (Sélenium)                   │
│                    ╱ ╲  Peu nombreux, très lents              │
│                   ╱   ╲                                       │
│                  ╱  Tests d'Intégration (test_api_flow.py)  │
│                 ╱    ╲  Nombreux, vitesse moyenne            │
│                ╱      ╲                                      │
│               ╱   Tests Unitaires (test_models, test_services) │
│              ╱         ╲  Beaucoup, très rapides              │
│             ╱___________ ╲                                    │
│                                                                 │
│  - Unitaires: Testent une fonction/classe isolée              │
│  - Intégration: Testent plusieurs composants ensemble         │
│  - E2E: Testent le système complet (utilisateur final)        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Votre Structure

```
grades_app/tests/
├── conftest.py          ← Fixtures réutilisables
├── factories.py         ← Factory Boy (création de données)
│
├── unit/
│   ├── test_models.py   ← Tests Unitaires (modèles isolés)
│   └── test_services.py ← Tests Unitaires (services isolés)
│
└── integration/
    └── test_api_flow.py ← Tests d'Intégration (workflows complets)
```

---

## Checklist d'Apprentissage

- [ ] Comprendre ce qu'est une **assertion** (`assert`)
- [ ] Savoir créer une **fonction de test** (commence par `test_`)
- [ ] Utiliser **Factory Boy** pour les données
- [ ] Créer et utiliser les **fixtures** avec `@pytest.fixture`
- [ ] Comprendre **@pytest.mark.django_db**
- [ ] Écrire des tests **unitaires** isolés
- [ ] Écrire des tests d'**intégration** avec API
- [ ] Utiliser le pattern **AAA** (Arrange-Act-Assert)
- [ ] Exécuter les tests avec `pytest grades_app/tests/ -v`
- [ ] Lire les rapports de **couverture** (`--cov`)

---

## Pour Aller Plus Loin

### Ressources

```bash
# Voir tous les tests
pytest grades_app/tests/ -v

# Voir avec couverture
pytest grades_app/tests/ --cov=grades_app --cov-report=html

# Tests d'un fichier spécifique
pytest grades_app/tests/unit/test_models.py -v

# Tests d'une classe spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel -v

# Tests d'une fonction spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel::test_student_creation_with_required_fields -v
```

### Différents types d'assertions utiles

```python
# Valeurs
assert value == 20
assert value != 0
assert value > 10
assert value <= 100

# Conteneurs
assert len(list) == 3
assert item in list
assert 'text' in string

# Existence
assert value is not None
assert obj.id is not None

# Booléens
assert condition is True
assert condition is False

# Exceptions
with pytest.raises(ValidationError):
    bad_object.full_clean()

# Regex
import re
assert re.match(r'^\d{8}$', matricule)
```

