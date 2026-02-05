# 🎨 Diagrammes et Visualisations des Concepts de Test

## Table des Matières
1. [Cycle de vie d'un test](#cycle-de-vie)
2. [Architecture des tests](#architecture)
3. [Factory Boy en détail](#factory-boy-visuel)
4. [Fixtures et dépendances](#fixtures-visuel)
5. [Pattern AAA](#pattern-aaa-visuel)
6. [Flux d'une assertion](#flux-assertion)
7. [Comparaison tests types](#comparaison-tests)
8. [Couverture de code](#couverture-visuel)

---

## Cycle de Vie d'un Test

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXÉCUTION D'UN TEST                          │
└─────────────────────────────────────────────────────────────────┘

1. DÉCOUVERTE
   └─ pytest cherche les fichiers test_*.py
   └─ pytest cherche les fonctions def test_*()
   └─ pytest cherche les classes TestXxx

2. SETUP (Préparation)
   └─ Créer une BD de test
   └─ Exécuter les fixtures
   └─ Initialiser les données

3. EXÉCUTION
   └─ Exécuter le test
   └─ Vérifier les assertions

4. TEARDOWN (Nettoyage)
   └─ Supprimer la BD de test
   └─ Libérer les ressources

5. RAPPORT
   └─ ✅ PASSED (réussi)
   └─ ❌ FAILED (échoué)
   └─ ⏭️  SKIPPED (ignoré)


EXEMPLE CONCRET:
═══════════════════════════════════════════════════════════════════

@pytest.mark.django_db                          ← Marqueur (dit à pytest que BD est nécessaire)
def test_student_creation():                    ← Nom du test
    # SETUP automatique: BD de test créée ✅
    
    student = StudentFactory()                  ← EXÉCUTION: créer Student
    
    assert student.id is not None               ← EXÉCUTION: vérifier
    
    # TEARDOWN automatique: BD supprimée ✅
    
    # RAPPORT: ✅ PASSED
```

---

## Architecture des Tests

```
┌─────────────────────────────────────────────────────────────────┐
│                    STRUCTURE DES TESTS                          │
└─────────────────────────────────────────────────────────────────┘

grades_app/
│
├── models.py              ← Code à tester (Production)
├── services.py            ← Services à tester (Production)
├── api/
│   └── views.py           ← API à tester (Production)
│
└── tests/                 ← 🧪 TESTS (Comme la production mais en test)
    │
    ├── conftest.py        ← Fixtures partagées
    │                       @pytest.fixture
    │                       def student():
    │                           return StudentFactory()
    │
    ├── factories.py        ← Création de données
    │                       class StudentFactory:
    │                           first_name = factory.Faker()
    │
    ├── unit/               ← Tests Unitaires (ISOLÉS)
    │   │
    │   ├── test_models.py  ← Tester: Student, Subject, Grade
    │   │                   └─ 20 tests
    │   │
    │   └── test_services.py ← Tester: generate_matricule, validate_grade
    │                          └─ 20 tests
    │
    └── integration/        ← Tests Intégration (ENSEMBLE)
        │
        └── test_api_flow.py ← Tester: API REST workflows
                              └─ 47 tests


INTERACTION:
═══════════════════════════════════════════════════════════════════

Test Unitaire                    Test Intégration
─────────────────────────────    ─────────────────────────────────

factory           StudentFactory                    APIClient
   │                 │                                 │
   ├─ Faker('name')  │                                 │
   └─ Sequence()     │                                 │
                     ▼                                 ▼
              StudentFactory.create()          POST /api/students/
                     │                                 │
                     ▼                                 ▼
              Student.objects.create()         Student.save()
                     │                                 │
                     ▼                                 ▼
              pytest DB isolation              APIClient → View
                     │                                 │
                     ▼                                 ▼
              assert student.id              assert response.status_code
                     │                                 │
                     ▼                                 ▼
              ✅ PASSED                        ✅ PASSED
              (rapide, isolé)                (lent, réaliste)
```

---

## Factory Boy Visuel

### Sans Factory Boy

```
Chaque test doit créer les données:

test_1: Student
  ├─ StudentFactory() → Student(first_name=X, last_name=Y, email=Z)
  └─ 5 lignes de setup

test_2: Student
  ├─ StudentFactory() → Student(first_name=X, last_name=Y, email=Z)
  └─ 5 lignes de setup

test_3: Student
  ├─ StudentFactory() → Student(first_name=X, last_name=Y, email=Z)
  └─ 5 lignes de setup

❌ Code répété 3 fois
❌ Si modèle change, tous les tests cassent
❌ Maintenance difficile
```

### Avec Factory Boy

```
Factory Boy génère les données:

class StudentFactory:
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f"student{n}@example.com")
    ↓
    StudentFactory() → Student(first_name='Alice', last_name='Dupont', email='student0@example.com')
    ↓
test_1: student = StudentFactory()
test_2: student = StudentFactory()
test_3: student = StudentFactory()

✅ Une seule définition
✅ Réutilisable partout
✅ Facile à maintenir
✅ Valeurs uniques et aléatoires
```

### Génération de valeurs

```
┌─────────────────────────────────────────────────────────────────┐
│              TYPES DE GÉNÉRATION DANS FACTORY BOY              │
└─────────────────────────────────────────────────────────────────┘

1. VALEUR FIXE
   ───────────────
   level = Student.LEVEL_L1
   
   Result:
   student1 = StudentFactory()  → level = "L1"
   student2 = StudentFactory()  → level = "L1"
   student3 = StudentFactory()  → level = "L1"
   
   Tous les tests: même valeur

2. ALÉATOIRE (Faker)
   ──────────────────
   first_name = factory.Faker('first_name')
   
   Result:
   student1 = StudentFactory()  → first_name = "Alice" (aléatoire)
   student2 = StudentFactory()  → first_name = "Bob"   (aléatoire)
   student3 = StudentFactory()  → first_name = "Charlie" (aléatoire)
   
   Chaque test: valeur différente et aléatoire

3. SÉQUENCE (Numérique)
   ────────────────────
   email = factory.Sequence(lambda n: f"student{n}@example.com")
   
   Result:
   student1 = StudentFactory()  → email = "student0@example.com"
   student2 = StudentFactory()  → email = "student1@example.com"
   student3 = StudentFactory()  → email = "student2@example.com"
   
   Chaque test: valeur unique numérotée

4. SUB-FACTORY (Relation)
   ──────────────────────
   student = factory.SubFactory(StudentFactory)
   
   Result:
   grade = GradeFactory()
   grade.student = Student créé automatiquement!
   grade.subject = Subject créé automatiquement!
   
   Les relations sont gérées automatiquement

5. LAZY FUNCTION (Dynamique)
   ──────────────────────────
   date = factory.LazyFunction(timezone.now)
   
   Result:
   grade1 = GradeFactory()  → date = 2026-02-05 11:30:00
   grade2 = GradeFactory()  → date = 2026-02-05 11:30:15
   
   Exécuté chaque fois (valeur à jour)
```

---

## Fixtures Visuel

### Dépendances entre fixtures

```
┌─────────────────────────────────────────────────────────────────┐
│           HIÉRARCHIE ET DÉPENDANCES DE FIXTURES                │
└─────────────────────────────────────────────────────────────────┘

conftest.py:

@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def subject():
    return SubjectFactory()


@pytest.fixture
def grade(student, subject):  ← Dépend de student ET subject!
    return GradeFactory(
        student=student,   ← Réutilise le student de la fixture
        subject=subject    ← Réutilise le subject de la fixture
    )


UTILISATION DANS UN TEST:
═══════════════════════════════════════════════════════════════════

def test_grade_with_fixtures(grade):
    # Reçoit:
    # - grade.student (créé par fixture student)
    # - grade.subject (créé par fixture subject)
    # - grade.value (10.0 par défaut)
    
    assert grade.student.id is not None      ✅ Student existe
    assert grade.subject.id is not None      ✅ Subject existe
    assert grade.value == 10.0               ✅ Grade a une note


FLUX INJECTION:
═══════════════════════════════════════════════════════════════════

pytest détecte test_grade_with_fixtures(grade)
         │
         ├─ Je dois fournir 'grade'
         │
         ├─ grade dépend de: student, subject
         │
         ├─ student ne dépend de rien
         │   → StudentFactory()
         │   → Return student
         │
         ├─ subject ne dépend de rien
         │   → SubjectFactory()
         │   → Return subject
         │
         ├─ grade dépend de: student, subject
         │   → GradeFactory(student=student, subject=subject)
         │   → Return grade
         │
         └─ test_grade_with_fixtures(grade)
            → Exécuter le test avec grade injecté
```

### Scopes de fixtures

```
┌─────────────────────────────────────────────────────────────────┐
│                PORTÉE DES FIXTURES (SCOPE)                     │
└─────────────────────────────────────────────────────────────────┘

scope="function" (par défaut)
──────────────────────────────
@pytest.fixture
def student():
    return StudentFactory()

test_1(student) → StudentFactory() → ✅ CRÉÉ
test_2(student) → StudentFactory() → ✅ CRÉÉ
test_3(student) → StudentFactory() → ✅ CRÉÉ

3 Student créés (une fois par test)
Avantage: Isolation totale
Désavantage: Plus lent


scope="class"
─────────────
@pytest.fixture(scope="class")
def student():
    return StudentFactory()

class TestStudent:
    def test_1(self, student) → ✅ Student1 (créé une fois)
    def test_2(self, student) → ✅ Student1 (réutilisé)
    def test_3(self, student) → ✅ Student1 (réutilisé)

1 Student créé pour toute la classe
Avantage: Plus rapide
Désavantage: Pas isolé (attention à l'ordre!)


scope="module"
──────────────
@pytest.fixture(scope="module")
def student():
    return StudentFactory()

test_models.py:
  test_1(student) → ✅ Student1 (créé une fois)
  test_2(student) → ✅ Student1 (réutilisé)

test_services.py:
  test_3(student) → ✅ Student2 (nouveau fichier = nouveau scope!)

1 Student par fichier
Avantage: Plus rapide
Désavantage: Pas isolé


scope="session"
───────────────
@pytest.fixture(scope="session")
def admin_user(db):
    return User.objects.create_superuser(...)

Toute la session de test:
  test_1(admin_user) → ✅ Admin1 (créé une fois)
  test_2(admin_user) → ✅ Admin1 (réutilisé)
  test_3(admin_user) → ✅ Admin1 (réutilisé)
  
1 User créé pour TOUS les tests!
Avantage: Beaucoup plus rapide
Désavantage: État partagé entre tous les tests ⚠️
```

---

## Pattern AAA Visuel

```
┌─────────────────────────────────────────────────────────────────┐
│                  PATTERN ARRANGE-ACT-ASSERT                    │
└─────────────────────────────────────────────────────────────────┘

STRUCTURE:
═════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_student_compute_general_average():
    """Tester le calcul de la moyenne générale."""
    
    # ┌───────────────────────────────────────────┐
    # │ ARRANGE - Préparer les données            │
    # └───────────────────────────────────────────┘
    student = StudentFactory()
    math = SubjectFactory(code='MATH', coefficient=2.0)
    physics = SubjectFactory(code='PHYS', coefficient=1.0)
    
    # Créer les notes
    GradeFactory(student=student, subject=math, value=16.0)
    GradeFactory(student=student, subject=physics, value=12.0)
    
    # État avant test:
    # student = Jean (id=1)
    #   ├─ Math 16.0 (coef 2.0)
    #   └─ Physics 12.0 (coef 1.0)
    
    # ┌───────────────────────────────────────────┐
    # │ ACT - Exécuter l'action                   │
    # └───────────────────────────────────────────┘
    average = student.compute_general_average()
    
    # Exécution:
    # 1. Récupérer toutes les notes de student
    # 2. Calculer: (16.0×2.0 + 12.0×1.0) / (2.0+1.0)
    # 3. Retourner: 14.67
    
    # ┌───────────────────────────────────────────┐
    # │ ASSERT - Vérifier le résultat             │
    # └───────────────────────────────────────────┘
    expected = round((16.0 * 2.0 + 12.0 * 1.0) / 3.0, 2)
    assert average == expected  # 14.67 == 14.67 ✅


EXEMPLE AVEC ERREUR:
═════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_student_cannot_have_grade_over_20():
    """Une note ne peut pas dépasser 20."""
    
    # ARRANGE
    student = StudentFactory()
    subject = SubjectFactory()
    
    # ACT & ASSERT - Ensemble pour les exceptions
    with pytest.raises(ValidationError):
        grade = Grade(student=student, subject=subject, value=25)
        grade.full_clean()
        
    # Flux:
    # 1. Créer Grade avec value=25
    # 2. Appeler full_clean() → trigger validation
    # 3. validate_grade(25) est appelé
    # 4. ValidationError levée ✅
    # 5. pytest.raises l'attrape ✅
    # 6. Test passe ✅
    
    
SANS pytest.raises (échouerait):
    grade = Grade(student=student, subject=subject, value=25)
    grade.full_clean()  # ValidationError levée!
    # Test s'arrête ❌ - pas de gestion de l'erreur
```

---

## Flux d'une Assertion

```
┌─────────────────────────────────────────────────────────────────┐
│                 EXÉCUTION D'UNE ASSERTION                       │
└─────────────────────────────────────────────────────────────────┘

Assertions simples:
═════════════════════════════════════════════════════════════════

assert student.first_name == "Alice"

│
├─ Évaluer: student.first_name == "Alice"
│  ├─ Accéder à student.first_name → "Alice"
│  ├─ Comparer à "Alice"
│  ├─ Résultat: True ✅
│
└─ PASSER AU TEST SUIVANT ✅


assert student.first_name == "Bob"

│
├─ Évaluer: student.first_name == "Bob"
│  ├─ Accéder à student.first_name → "Alice"
│  ├─ Comparer à "Bob"
│  ├─ Résultat: False ❌
│
├─ LEVER EXCEPTION: AssertionError
├─ AFFICHER MESSAGE: AssertionError: assert "Alice" == "Bob"
└─ ARRÊTER LE TEST ❌


Assertions avec exceptions:
═════════════════════════════════════════════════════════════════

with pytest.raises(ValidationError):
    grade = Grade(student=student, subject=subject, value=25)
    grade.full_clean()

│
├─ Entrer dans le contexte pytest.raises(ValidationError)
│  "Je m'attends à ce qu'une ValidationError soit levée"
│
├─ Exécuter le code:
│  ├─ Créer Grade(value=25)
│  ├─ Appeler full_clean()
│  ├─ validate_grade(25) exécuté
│  ├─ ValidationError levée ✅
│
├─ pytest.raises l'attrape
├─ C'est ce qu'on attendait ✅
└─ PASSER AU TEST SUIVANT ✅


with pytest.raises(ValidationError):
    grade = Grade(student=student, subject=subject, value=15)
    grade.full_clean()  # Pas d'erreur!

│
├─ Entrer dans le contexte pytest.raises(ValidationError)
│
├─ Exécuter le code:
│  ├─ Créer Grade(value=15)
│  ├─ Appeler full_clean()
│  ├─ validate_grade(15) exécuté
│  ├─ Pas d'erreur ✅ (15 est valide)
│
├─ Aucune exception levée ❌
├─ pytest.raises attendait une ValidationError
└─ ARRÊTER LE TEST - ÉCHOUE ❌
   Message: "DID NOT RAISE ValidationError"
```

---

## Comparaison Tests Types

```
┌─────────────────────────────────────────────────────────────────┐
│              COMPARAISON VISUELLE DES TYPES DE TEST            │
└─────────────────────────────────────────────────────────────────┘

TEST UNITAIRE:
═════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_student_creation():
    """Tester Student isolément."""
    
    student = StudentFactory()
    assert student.id is not None

Scope:          Une classe/fonction uniquement
Vitesse:        ⚡ Très rapide (< 1ms)
Isolation:      ✅ Complète
Dépendances:    Aucune (test l'objet seul)
Maintenance:    ✅ Facile
Fiabilité:      Partielle (ne teste pas interactions)

Analogie:       Tester qu'une roue d'une voiture tourne


TEST D'INTÉGRATION:
═════════════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_create_student_and_get_average_via_api(client):
    """Test du workflow complet."""
    
    # Créer Student via API
    response = client.post('/api/students/', {...})
    student_id = response.data['id']
    
    # Créer Subject via API
    response = client.post('/api/subjects/', {...})
    subject_id = response.data['id']
    
    # Ajouter Grade via API
    client.post('/api/grades/', {...})
    
    # Vérifier la moyenne
    response = client.get(f'/api/students/{student_id}/average/')
    assert response.data['average'] == 15.5

Scope:          Plusieurs composants ensemble
Vitesse:        🐢 Plus lent (~ 100ms)
Isolation:      ❌ Non isolé (plusieurs systèmes)
Dépendances:    API → Services → Models → BD
Maintenance:    ❌ Difficile (cascade d'erreurs)
Fiabilité:      ✅ Très élevée (teste interactions réelles)

Analogie:       Tester que la voiture entière fonctionne


TEST E2E (Selenium):
═════════════════════════════════════════════════════════════════

def test_user_interface_flow():
    """Tester l'application complète via navigateur."""
    
    driver = webdriver.Chrome()
    driver.get('http://localhost:8888/admin/')
    
    # Login
    driver.find_element(By.ID, 'username').send_keys('admin')
    driver.find_element(By.ID, 'password').send_keys('pass')
    driver.find_element(By.CSS_SELECTOR, 'button').click()
    
    # Créer étudiant
    # Ajouter note
    # Vérifier dans l'interface
    
    driver.quit()

Scope:          L'application entière + Interface utilisateur
Vitesse:        🐌 Très lent (~ 5-10 secondes par test)
Isolation:      ❌ Très peu isolé
Dépendances:    Navigateur → Interface → API → BD
Maintenance:    ❌❌ Très difficile
Fiabilité:      ✅✅ Confiance maximale (imite utilisateur réel)

Analogie:       Donner la voiture à quelqu'un et voir s'il peut conduire


PYRAMIDE:
═════════════════════════════════════════════════════════════════

           ▲
          ╱│╲
         ╱ │ ╲          E2E Tests (Selenium)
        ╱  │  ╲         Peu nombreux, très lents
       ╱   │   ╲        Confiants mais fragiles
      ╱────┼────╲
     ╱     │     ╲      Tests Intégration
    ╱      │      ╲     Nombreux, vitesse moyenne
   ╱       │       ╲    Fiables et maintenables
  ╱────────┼────────╲
 ╱         │         ╲  Tests Unitaires
╱          │          ╲ Très nombreux, très rapides
____________│___________\ Maintenables et simples
            │
            │
          Base
```

---

## Couverture de Code Visuel

```
┌─────────────────────────────────────────────────────────────────┐
│                  COUVERTURE DE CODE (COVERAGE)                 │
└─────────────────────────────────────────────────────────────────┘

Qu'est-ce que c'est?
════════════════════════════════════════════════════════════════

La couverture mesure: "Quel pourcentage du code est testé?"


EXEMPLE VISUEL:
════════════════════════════════════════════════════════════════

Code (models.py):
─────────────────
class Student:
    def __init__(self, first_name):
        self.first_name = first_name     ← Ligne 1 (tester ça?)
    
    def full_name(self):
        if self.first_name:              ← Ligne 2 (tester ça?)
            return self.first_name       ← Ligne 3 (tester ça?)
        return "Unknown"                 ← Ligne 4 (tester ça?)


TEST INCOMPLET:
───────────────
def test_student():
    student = Student("Alice")
    ✅ Ligne 1 couverte (Student.__init__ exécuté)
    ✅ Ligne 2 couverte (if exécuté avec True)
    ✅ Ligne 3 couverte (return exécuté)
    ❌ Ligne 4 NON couverte (else jamais exécuté)

Couverture: 3/4 = 75%
Missing: 4 (ligne return "Unknown")


TEST COMPLET:
─────────────
def test_student_with_name():
    student = Student("Alice")
    ✅ Ligne 1
    ✅ Ligne 2 (True)
    ✅ Ligne 3

def test_student_without_name():
    student = Student(None)
    ✅ Ligne 1
    ✅ Ligne 2 (False)
    ✅ Ligne 4

Couverture: 4/4 = 100%
Missing: Aucune


RAPPORT VISUEL:
════════════════════════════════════════════════════════════════

Votre couverture: 97% (859/906 lignes)

█████████████████████████████████████████ 97%

Répartition:
├─ models.py:      100% ██████████████████████████████████████████
├─ services.py:    100% ██████████████████████████████████████████
├─ api/views.py:   100% ██████████████████████████████████████████
├─ api/serializers: 95% ███████████████████████████████████████░░░
└─ other:          92% ██████████████████████████████████░░░░░░░░


INTERPRÉTATION:
════════════════════════════════════════════════════════════════

90-100% → Excellent! ✅
80-90%  → Bon (un peu d'amélioration possible)
70-80%  → Acceptable (mais attention aux bugs)
<70%    → Mauvais! (trop de code non testé)


97% = Excellent! 🎉
```

---

## Diagramme Flux: Création et Test d'un Student

```
┌─────────────────────────────────────────────────────────────────┐
│        FLUX COMPLET: CRÉER ET TESTER UN STUDENT                │
└─────────────────────────────────────────────────────────────────┘


1. SETUP (Avant le test):
════════════════════════════════════════════════════════════════

pytest découvre:
├─ test_student_creation()
├─ @pytest.mark.django_db
└─ Fixture student (optionnel)

pytest prépare:
├─ Créer une BD de test
├─ Passer la BD à Django
├─ Prêt pour l'exécution


2. EXÉCUTION (Pendant le test):
════════════════════════════════════════════════════════════════

test_student_creation():
│
├─ student = StudentFactory()
│  │
│  ├─ StudentFactory détecte create()
│  │
│  ├─ Générer les champs:
│  │  ├─ first_name = Faker('first_name') → "Alice"
│  │  ├─ last_name = Faker('last_name') → "Dupont"
│  │  ├─ email = Sequence(0) → "student0@example.com"
│  │  ├─ level = Student.LEVEL_L1 → "L1"
│  │
│  ├─ Créer Student(first_name="Alice", ...)
│  │
│  ├─ Appeler Student.save()
│  │  ├─ Vérifier unique_together (email)
│  │  ├─ Insérer en BD
│  │  └─ Affecter l'ID: 1
│  │
│  └─ Retourner Student(id=1, ...)
│
├─ assert student.id is not None
│  ├─ Évaluer: student.id is not None
│  ├─ student.id = 1 ✅
│  ├─ 1 is not None = True ✅
│  └─ Assertion passe ✅
│
└─ Fin du test


3. TEARDOWN (Après le test):
════════════════════════════════════════════════════════════════

pytest nettoie:
├─ Supprimer la BD de test
├─ Libérer la mémoire
├─ Revenir à l'état initial

Résultat:
├─ test_student_creation: ✅ PASSED


4. RAPPORT:
════════════════════════════════════════════════════════════════

pytest affiche:
---
tests/unit/test_models.py::TestStudentModel::test_student_creation PASSED [100%]
---

1 passed in 0.05s ✅
```

---

## Résumé Visuel: Tous les Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│             RÉSUMÉ VISUEL DE TOUS LES CONCEPTS                 │
└─────────────────────────────────────────────────────────────────┘


PYTEST FRAMEWORK
════════════════════════════════════════════════════════════════

pytest   ← Exécute les tests
  ├─ @pytest.fixture          ← Crée des données réutilisables
  ├─ @pytest.mark.django_db   ← BD de test pour Django
  ├─ pytest.raises()          ← Vérifie les exceptions
  └─ assert                   ← Vérifie les conditions


FACTORY BOY
════════════════════════════════════════════════════════════════

Factory Bo ← Crée les données de test rapidement
  ├─ factory.Faker()          ← Valeurs aléatoires réalistes
  ├─ factory.Sequence()       ← Valeurs uniques numérotées
  ├─ factory.SubFactory()     ← Relations automatiques
  └─ .create_batch(n)         ← Créer plusieurs à la fois


TESTS UNITAIRES (test_models.py, test_services.py)
════════════════════════════════════════════════════════════════

Un test isolé    ← Teste UNE classe/fonction
  ├─ Rapide      ← < 1ms chacun
  ├─ Simple      ← Facile à écrire
  ├─ Isolé       ← Ne dépend de rien
  └─ Maintenable ← Facile à modifier


TESTS INTÉGRATION (test_api_flow.py)
════════════════════════════════════════════════════════════════

Plusieurs tests ensemble    ← Teste les interactions
  ├─ Lent                   ← ~100ms chacun
  ├─ Complexe               ← Plus à mettre en place
  ├─ Non isolé              ← Dépend de plusieurs systèmes
  └─ Fiable                 ← Détecte les vrais bugs


PATTERN AAA
════════════════════════════════════════════════════════════════

ARRANGE  ← Préparer les données
ACT      ← Exécuter ce qu'on teste
ASSERT   ← Vérifier le résultat


ASSERTIONS
════════════════════════════════════════════════════════════════

assert value == expected                ← Égalité
assert value is not None                ← Existence
assert item in list                     ← Membership
with pytest.raises(ErrorType):          ← Exception
    code_that_should_error()


COUVERTURE
════════════════════════════════════════════════════════════════

% du code testé
├─ 100%: Parfait 🎉
├─ 90-100%: Excellent ✅
├─ 80-90%: Bon
├─ <80%: À améliorer ⚠️

Votre projet: 97% ✅✅
```

