# 🎓 Exercices Pratiques - Apprendre les Concepts de Test

## Comment utiliser ce guide?

1. **Lisez** la théorie dans `TEST_CONCEPTS_GUIDE.md`
2. **Pratiquez** avec les exercices ci-dessous
3. **Validez** en exécutant `pytest`
4. **Comprenez** en lisant le code existant

---

## Exercice 1: Votre Premier Test

### Objectif
Créer un test simple qui vérifie qu'un Student peut être créé.

### Code à comprendre
```python
# Ce test crée un Student et vérifie qu'il a un ID
@pytest.mark.django_db
def test_student_creation_simple():
    """Créer un student et vérifier qu'il a un ID."""
    student = StudentFactory()
    assert student.id is not None
```

### Pourquoi `@pytest.mark.django_db`?
- **Raison:** Ce test accède à la base de données (sauvegarde de Student)
- **Sans ça:** pytest lèverait une erreur `RuntimeError`
- **Avec ça:** pytest crée une BD isolée pour le test

### Pourquoi `assert student.id is not None`?
- **`assert`:** Vérifier une condition
- **`is not None`:** L'ID existe et n'est pas vide
- **Si échoue:** pytest dit "AssertionError" et affiche le problème

### À faire
Allez dans `grades_app/tests/unit/test_models.py` et trouvez ce test:
```python
@pytest.mark.django_db
def test_student_creation_with_required_fields(self):
    student = StudentFactory(...)
    assert student.id is not None
```

---

## Exercice 2: Tester la Validation

### Objectif
Comprendre comment vérifier qu'une erreur est levée.

### Code à comprendre
```python
# Cette note est INVALIDE (25 > 20)
# Ce test DOIT générer une erreur
with pytest.raises(ValidationError):
    grade = Grade(student=student, subject=subject, value=25)
    grade.full_clean()  # Déclenche la validation
```

### Structure
```
with pytest.raises(ValidationError):  # Attendre une erreur
    code_qui_cause_erreur()           # Exécuter le code
    # Si AUCUNE erreur -> test échoue ❌
    # Si ValidationError -> test réussit ✅
    # Si autre erreur -> test échoue ❌
```

### Scenario
- **Grade 25**: Pas valide → ValidationError levée → Test passe ✅
- **Grade 15**: Valide → Pas d'erreur → Test échoue ❌

### À faire
Allez dans `grades_app/tests/unit/test_models.py` et trouvez les tests:
```python
def test_grade_value_cannot_be_negative(self):
def test_grade_value_cannot_exceed_twenty(self):
```

---

## Exercice 3: Utiliser les Fixtures

### Objectif
Comprendre comment réutiliser les données de test.

### Sans Fixture (❌ Répétitif)
```python
def test_student_1():
    student = StudentFactory()
    assert student.id is not None

def test_student_2():
    student = StudentFactory()  # Même code!
    assert student.first_name is not None
```

### Avec Fixture (✅ Réutilisable)
```python
@pytest.fixture
def student():
    return StudentFactory()

def test_student_1(student):  # Reçoit la fixture!
    assert student.id is not None

def test_student_2(student):  # Même fixture!
    assert student.first_name is not None
```

### Fichier: conftest.py
```python
@pytest.fixture
def student():
    """Crée un Student pour les tests."""
    return StudentFactory()

@pytest.fixture
def grade(student):  # Dépend de student!
    """Crée une Grade avec le Student."""
    return GradeFactory(student=student)
```

### À faire
1. Ouvrez `conftest.py`
2. Trouvez les fixtures existantes
3. Comprenez les dépendances (grade → student, subject)

---

## Exercice 4: Factory Boy - Créer des Données

### Objectif
Comprendre comment Factory Boy crée les données automatiquement.

### Problème: Sans Factory
```python
@pytest.mark.django_db
def test_multiple_students():
    student1 = Student.objects.create(
        first_name="Alice",
        last_name="Dupont",
        email="alice@example.com",
        level="L1"
    )
    student2 = Student.objects.create(
        first_name="Bob",
        last_name="Martin",
        email="bob@example.com",
        level="L1"
    )
    # Beaucoup de code répétitif!
```

### Solution: Avec Factory
```python
@pytest.mark.django_db
def test_multiple_students():
    students = StudentFactory.create_batch(2)  # 2 students en 1 ligne!
    assert len(students) == 2
    assert students[0].id is not None
    assert students[1].id is not None
```

### Fonctionnement de Factory Boy

**Fichier: factories.py**
```python
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student  # Quel modèle créer?
    
    # Ces champs se remplissent AUTOMATIQUEMENT
    first_name = factory.Faker('first_name')  # Nom aléatoire
    last_name = factory.Faker('last_name')    # Prénom aléatoire
    email = factory.Sequence(lambda n: f"student{n}@example.com")
```

### Résultat
```python
student1 = StudentFactory()
# Résultat:
# first_name = "Alice" (aléatoire)
# last_name = "Dupont" (aléatoire)
# email = "student0@example.com" (unique!)

student2 = StudentFactory()
# Résultat:
# first_name = "Bob" (aléatoire, différent)
# last_name = "Martin" (aléatoire, différent)
# email = "student1@example.com" (unique!)
```

### À faire
Ouvrez `factories.py` et comprenez:
- `factory.Faker('first_name')` → génère des noms aléatoires
- `factory.Sequence(lambda n: ...)` → génère des valeurs uniques
- `factory.SubFactory(StudentFactory)` → crée automatiquement un Student

---

## Exercice 5: Pattern AAA (Arrange-Act-Assert)

### Objectif
Organiser les tests de manière cohérente.

### Pattern AAA
```
ARRANGE - Préparer les données
ACT     - Exécuter l'action
ASSERT  - Vérifier le résultat
```

### Exemple complet
```python
@pytest.mark.django_db
def test_student_compute_general_average():
    # ARRANGE - Créer les données
    student = StudentFactory()
    math = SubjectFactory(code='MATH', coefficient=2.0)
    phys = SubjectFactory(code='PHYS', coefficient=1.0)
    GradeFactory(student=student, subject=math, value=20.0)  # 20 en Math
    GradeFactory(student=student, subject=phys, value=10.0)  # 10 en Physique
    
    # ACT - Exécuter ce qu'on teste
    result = student.compute_general_average()
    
    # ASSERT - Vérifier
    # Moyenne = (20×2 + 10×1) / (2+1) = 50/3 = 16.67
    assert result == 16.67
```

### Avantages
1. **Lisibilité:** Clair ce qu'on prépare, exécute, vérifie
2. **Maintenabilité:** Facile de modifier une partie
3. **Débogage:** Si ça échoue, on sait où regarder

### À faire
1. Ouvrez `test_models.py`
2. Trouvez un test avec le pattern AAA
3. Identifiez les 3 sections avec des commentaires

---

## Exercice 6: Tests Unitaires vs Intégration

### Unitaire = Une chose isolée

```python
# test_models.py - UNITAIRE
@pytest.mark.django_db
def test_student_creation():
    """Teste JUSTE la création du Student."""
    student = StudentFactory()
    assert student.id is not None
    # On teste le modèle isolément
```

**Caractéristiques:**
- ✅ Très rapide (< 1ms)
- ✅ Facile à écrire
- ❌ Ne teste pas les vraies interactions

### Intégration = Tout ensemble

```python
# test_api_flow.py - INTÉGRATION
@pytest.mark.django_db
def test_full_workflow(client):
    """Test un workflow complet."""
    
    # 1. Créer un Student via API
    response = client.post('/api/students/', {
        'first_name': 'Alice',
        'last_name': 'Dupont',
        'level': 'L1',
        'email': 'alice@example.com'
    })
    student_id = response.data['id']
    
    # 2. Créer une Subject
    response = client.post('/api/subjects/', {
        'code': 'MATH',
        'name': 'Mathématiques',
        'coefficient': 2.0
    })
    subject_id = response.data['id']
    
    # 3. Ajouter une Grade
    response = client.post('/api/grades/', {
        'student': student_id,
        'subject': subject_id,
        'value': 18.5
    })
    
    # 4. Vérifier la moyenne
    response = client.get(f'/api/students/{student_id}/average/')
    assert response.data['average'] == 18.5
```

**Caractéristiques:**
- ✅ Teste les vraies interactions
- ❌ Plus lent
- ❌ Plus difficile à déboguer

### À faire
1. Comparez `test_models.py` (unitaire) et `test_api_flow.py` (intégration)
2. Remarquez la différence de complexité
3. Comprenez pourquoi les deux sont nécessaires

---

## Exercice 7: Comprendre les Assertions

### Types d'assertions

```python
# 1. Égalité
assert student.first_name == "Alice"
assert grade.value == 15.5

# 2. Existence
assert student.id is not None
assert student.email is not None

# 3. Comparaison
assert grade.value > 10
assert grade.value <= 20

# 4. Conteneurs
assert len(students) == 3
assert 'L1' in [Student.LEVEL_L1, Student.LEVEL_L2]

# 5. Exceptions
with pytest.raises(ValidationError):
    grade = Grade(value=25)
    grade.full_clean()

# 6. Chaînes
assert "Alice" in str(student)
import re
assert re.match(r'^\d{8}$', student.matricule)
```

### Message d'erreur amélioré

```python
# ❌ Mauvais - message confus
assert len(students) == 5

# ✅ Bon - message clair
assert len(students) == 5, f"Expected 5 students, got {len(students)}"
```

### À faire
Allez dans `test_models.py` et trouvez 5 types d'assertions différentes.

---

## Exercice 8: Decorator @pytest.mark.django_db

### Qu'est-ce que c'est?

C'est une **annotation** qui dit à pytest: "Ce test accède à la base de données"

### Pourquoi c'est important?

```python
# ❌ SANS @pytest.mark.django_db
def test_student():
    student = StudentFactory()  # RuntimeError!
    # pytest ne sait pas qu'on veut une BD

# ✅ AVEC @pytest.mark.django_db
@pytest.mark.django_db
def test_student():
    student = StudentFactory()  # OK! BD créée
```

### Variantes

```python
# Par défaut - une transaction par test (rapide)
@pytest.mark.django_db
def test_student():
    StudentFactory()  # Dans une transaction
    # Auto-rollback après

# Transactions réelles (plus lent, plus fiable)
@pytest.mark.django_db(transaction=True)
def test_with_real_transactions():
    pass
```

### À faire
1. Ouvrez `test_models.py`
2. Vérifiez que TOUS les tests ont `@pytest.mark.django_db`
3. Comprenez pourquoi

---

## Exercice 9: Exécuter les Tests

### Commandes basiques

```bash
# Tous les tests
pytest grades_app/tests/ -v

# Un fichier spécifique
pytest grades_app/tests/unit/test_models.py -v

# Une classe spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel -v

# Un test spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel::test_student_creation_with_required_fields -v
```

### Avec couverture

```bash
# Voir la couverture
pytest grades_app/tests/ --cov=grades_app --cov-report=term-missing

# HTML interactif
pytest grades_app/tests/ --cov=grades_app --cov-report=html
# Puis ouvrir: htmlcov/index.html
```

### À faire
1. Exécutez: `pytest grades_app/tests/ -v`
2. Regardez la sortie
3. Exécutez: `pytest grades_app/tests/unit/test_models.py::TestStudentModel::test_student_creation_with_required_fields -v`
4. Remarquez la sortie détaillée

---

## Exercice 10: Lire et Comprendre le Code Existant

### Fichiers à lire

1. **factories.py** (10 min)
   - Comprendre StudentFactory, SubjectFactory, GradeFactory
   - Voir comment Faker et Sequence fonctionnent

2. **conftest.py** (5 min)
   - Voir les fixtures disponibles
   - Comprendre les dépendances

3. **test_models.py** (20 min)
   - TestStudentModel: création, email unique, matricule
   - TestSubjectModel: création, code unique
   - TestGradeModel: validation, unique_together

4. **test_services.py** (15 min)
   - TestGenerateMatricule: format, incrémentation
   - TestValidateGrade: validation 0-20
   - TestComputeSubjectAverage: calculs avec coefficients

5. **test_api_flow.py** (20 min)
   - TestAPIAuthentication: auth requise
   - TestStudentAPI: CRUD via API
   - Workflows complets

### Checklist de compréhension

- [ ] Je comprends pourquoi chaque test utilise `@pytest.mark.django_db`
- [ ] Je peux nommer les 3 sections du pattern AAA
- [ ] Je sais pourquoi les fixtures sont réutilisables
- [ ] Je comprends comment Factory Boy génère les données
- [ ] Je sais la différence entre unitaire et intégration
- [ ] Je peux lire une assertion et savoir ce qu'elle teste

---

## Quiz - Testez Votre Compréhension!

### Question 1: Fixtures
Qu'est-ce qu'une fixture?
```
A) Un test qui est toujours échoué
B) Une fonction réutilisable qui crée des données pour les tests
C) Un framework de test
D) Une erreur dans le code
```
**Réponse:** B

### Question 2: Factory Boy
Qu'est-ce que `factory.Sequence`?
```
A) Créer plusieurs objets en séquence
B) Générer des valeurs uniques (0, 1, 2, ...)
C) Exécuter les tests dans l'ordre
D) Créer une sauvegarde des données
```
**Réponse:** B

### Question 3: Assertions
Qu'est-ce que `pytest.raises`?
```
A) Lever une exception
B) Vérifier qu'une exception EST levée
C) Vérifier qu'une exception N'EST PAS levée
D) Arrêter le test
```
**Réponse:** B

### Question 4: Pattern AAA
Quel est l'ordre correct?
```
A) Assert, Arrange, Act
B) Act, Assert, Arrange
C) Arrange, Act, Assert
D) Assert, Act, Arrange
```
**Réponse:** C

### Question 5: Test Types
Quel est un test unitaire?
```
A) Créer un étudiant via API, ajouter une note, vérifier la moyenne
B) Créer un Student et vérifier qu'il a un ID
C) Créer 100 étudiants et vérifier l'API
D) Tester toute l'application
```
**Réponse:** B

---

## Prochaines Étapes

### Niveau 1: Compréhension (Vous êtes ici!)
- [ ] Lire `TEST_CONCEPTS_GUIDE.md`
- [ ] Faire les exercices 1-10
- [ ] Réussir le quiz

### Niveau 2: Écriture
- [ ] Écrire un test simple
- [ ] Créer une fixture
- [ ] Écrire 5 tests pour une nouvelle fonctionnalité

### Niveau 3: Mastery
- [ ] Comprendre la couverture de code
- [ ] Écrire des tests d'intégration complets
- [ ] Déboguer les tests qui échouent

---

## Ressources Utiles

### Documentation
- pytest: https://docs.pytest.org/
- Factory Boy: https://factoryboy.readthedocs.io/
- Django Testing: https://docs.djangoproject.com/en/4.2/topics/testing/

### Commandes
```bash
# Tous les tests
pytest grades_app/tests/ -v

# Avec couverture
pytest grades_app/tests/ --cov=grades_app --cov-report=term-missing

# Un test spécifique
pytest grades_app/tests/unit/test_models.py::TestStudentModel::test_student_creation_with_required_fields -v

# Arrêter au premier échec
pytest grades_app/tests/ -x

# Afficher les prints
pytest grades_app/tests/ -s

# Tests lents
pytest grades_app/tests/ --durations=10
```

### FAQ

**Q: Pourquoi @pytest.mark.django_db?**
A: Django a besoin d'une base de données isolée pour chaque test.

**Q: Pourquoi Factory Boy?**
A: Pour ne pas répéter le code de création de données.

**Q: Unitaire ou Intégration?**
A: Les deux! Unitaire pour la vitesse, intégration pour la confiance.

**Q: Comment déboguer un test qui échoue?**
A: Utilisez `pytest -s` pour voir les prints, puis lire le message d'erreur.

