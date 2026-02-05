# 📚 Grades App

Module Django complet pour la gestion des étudiants, matières et notes avec API REST.

## 🚀 Démarrage rapide avec Docker

### Prérequis
- Docker et Docker Compose installés
- Port 8000 disponible (API Django)
- Port 5432 disponible (PostgreSQL)

### Lancer l'application

**Option 1: Script de démarrage**
```bash
chmod +x start.sh
./start.sh
```

**Option 2: Docker Compose direct**
```bash
docker-compose up --build
```

**Option 3: Makefile**
```bash
make up
```

### Accès à l'application
- **API REST**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **Base de données**: `localhost:5432`

### Identifiants par défaut
- **Utilisateur admin**: `admin`
- **Mot de passe**: `admin123`

## 📊 Commandes utiles

### Avec Make
```bash
make help          # Afficher l'aide
make build         # Construire les images
make up            # Démarrer l'app
make down          # Arrêter l'app
make logs          # Voir les logs
make test          # Lancer les tests
make test-coverage # Tests avec couverture
make clean         # Nettoyer les conteneurs
```

### Avec Docker Compose
```bash
docker-compose build                    # Construire
docker-compose up                       # Démarrer
docker-compose down                     # Arrêter
docker-compose logs -f                  # Logs en direct
docker-compose exec web pytest          # Tests
docker-compose exec web python manage.py shell  # Shell Django
```

## 🏗️ Structure du projet

```
grades_app/
├── config/                 # Configuration Django
├── grades_app/
│   ├── api/               # API REST (ViewSets, Serializers, Permissions)
│   ├── migrations/        # Migrations de base de données
│   ├── tests/             # Tests unitaires et d'intégration
│   ├── models.py          # Modèles (Student, Subject, Grade)
│   └── services.py        # Logique métier
├── docker-compose.yml     # Configuration Docker
├── Dockerfile             # Image Docker
├── entrypoint.sh          # Script de démarrage
├── Makefile              # Commandes utiles
└── requirements.txt       # Dépendances Python
```

## 👥 Rôles et permissions

### Admin (is_staff)
- Accès complet à l'API et l'admin Django
- CRUD complet sur tous les modèles

### Enseignant (groupe `enseignant`)
- CRUD sur étudiants
- CRUD sur matières  
- CRUD sur les notes

### Étudiant (groupe `etudiant`)
- Accès lecture seule à ses données
- Voir ses notes et sa moyenne générale

## 📋 Modèles de données

### Student
- `matricule`: Identifiant unique généré automatiquement
- `first_name`: Prénom
- `last_name`: Nom
- `level`: Niveau (L1, L2, L3, M1, M2)
- `email`: Email unique
- `created_at`: Date de création

### Subject
- `code`: Code unique (ex: MATH101)
- `name`: Nom de la matière
- `coefficient`: Coefficient de pondération

### Grade
- `student`: ForeignKey vers Student
- `subject`: ForeignKey vers Subject
- `value`: Note (0-20)
- `date`: Date de la note
- `comment`: Commentaire optionnel

## 🧪 Tests

Les tests sont organisés en deux catégories:

### Tests unitaires
```bash
docker-compose exec web pytest grades_app/tests/unit/
```

### Tests d'intégration
```bash
docker-compose exec web pytest grades_app/tests/integration/
```

### Couverture de code
```bash
docker-compose exec web pytest --cov=grades_app --cov-report=html
# Rapport généré dans htmlcov/index.html
```

## 🔒 Sécurité

### Bandit (détection de vulnérabilités)
```bash
docker-compose exec web bandit -r grades_app
```

## 🌱 Population de données de test

Les données sont créées automatiquement au premier démarrage:
- 5 étudiants de différents niveaux
- 5 matières avec différents coefficients
- Notes pour chaque étudiant/matière

Pour repeupler manuellement:
```bash
docker-compose exec web python manage.py shell < scripts/seed.py
```

## 📝 API Endpoints

### Students
- `GET /api/students/` - Lister les étudiants
- `POST /api/students/` - Créer un étudiant
- `GET /api/students/{id}/` - Détail d'un étudiant
- `PUT /api/students/{id}/` - Modifier un étudiant
- `DELETE /api/students/{id}/` - Supprimer un étudiant
- `GET /api/students/{id}/average/` - Moyenne de l'étudiant

### Subjects
- `GET /api/subjects/` - Lister les matières
- `POST /api/subjects/` - Créer une matière
- `GET /api/subjects/{id}/` - Détail d'une matière
- `PUT /api/subjects/{id}/` - Modifier une matière
- `DELETE /api/subjects/{id}/` - Supprimer une matière

### Grades
- `GET /api/grades/` - Lister les notes
- `POST /api/grades/` - Créer une note
- `GET /api/grades/{id}/` - Détail d'une note
- `PUT /api/grades/{id}/` - Modifier une note
- `DELETE /api/grades/{id}/` - Supprimer une note

## 🐛 Dépannage

### Port 8000 déjà utilisé
```bash
docker-compose down
# ou spécifier un port différent dans docker-compose.yml
```

### Erreurs de base de données
```bash
docker-compose down -v  # Supprime les volumes
docker-compose up --build  # Recommence de zéro
```

### Accéder à la base de données
```bash
docker-compose exec db psql -U grades_user -d grades_app
```

## 📚 Structure des tests

- `grades_app/tests/unit/`: tests unitaires des services et modèles
- `grades_app/tests/integration/`: tests d'API end-to-end
- `grades_app/tests/factories.py`: factories Factory Boy
- `grades_app/tests/conftest.py`: fixtures pytest
