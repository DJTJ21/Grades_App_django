# 🚀 Guide de démarrage - Grades App

## ✅ Prérequis vérifiés

L'application **Grades App** a été configurée pour fonctionner entièrement dans Docker. Voici ce qui a été préparé:

- ✅ Dockerfile optimisé (python:3.11-slim)
- ✅ Docker Compose avec PostgreSQL 15
- ✅ Script d'entrypoint avec:
  - Attente de la base de données
  - Application automatique des migrations
  - Création du superutilisateur
  - Population de données de test
- ✅ Migrations Django pré-généées (0001_initial.py)
- ✅ API REST complète avec permissions
- ✅ Tests unitaires et d'intégration

## 🎯 Démarrer l'application

### Étape 1: Arrêter le processus actuel (si en cours)

```bash
# Dans un autre terminal
cd /home/romuald/Downloads/grades_app
Ctrl+C  # Si le docker compose est en cours
```

### Étape 2: Nettoyer les anciens conteneurs

```bash
docker compose down -v
```

### Étape 3: Démarrer l'application

```bash
cd /home/romuald/Downloads/grades_app
docker compose up --build
```

## 📊 Vérifier que ça marche

Une fois que vous voyez:
```
Starting Django application
Quit the server with CONTROL-C.
```

### Tester l'API dans un autre terminal:

```bash
# Liste des étudiants
curl http://localhost:8000/api/students/

# Liste des matières
curl http://localhost:8000/api/subjects/

# Liste des notes
curl http://localhost:8000/api/grades/
```

### Accéder à l'interface web:

- **Admin Django**: http://localhost:8000/admin/
  - Utilisateur: `admin`
  - Mot de passe: `admin123`

- **API**: http://localhost:8000/api/
  - Browsable API avec interface interactive

## 📋 Commandes principales

### Avec Docker Compose

```bash
# Démarrer
docker compose up --build

# Démarrer en arrière-plan
docker compose up -d --build

# Arrêter
docker compose down

# Voir les logs
docker compose logs -f

# Accéder au shell Django
docker compose exec web python manage.py shell

# Lancer les tests
docker compose exec web pytest

# Lancer les tests avec couverture
docker compose exec web pytest --cov=grades_app --cov-report=html
```

### Avec Make (plus simple)

```bash
make up              # Démarrer
make down            # Arrêter
make logs            # Voir les logs
make test            # Lancer les tests
make test-coverage   # Tests avec couverture
make clean           # Nettoyer tout
```

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      Docker Compose Network         │
│                                     │
│  ┌──────────────┐  ┌────────────┐  │
│  │  PostgreSQL  │  │   Django   │  │
│  │   (Port:     │  │   (Port:   │  │
│  │   5432)      │  │   8000)    │  │
│  └──────────────┘  └────────────┘  │
│                                     │
│   Volumes:                          │
│   - postgres_data (persistence)     │
│   - . (live reload code)            │
│                                     │
└─────────────────────────────────────┘
```

## 📊 Base de données

### Données initiales créées automatiquement:

**Étudiants:**
- Jean Dupont (L1)
- Marie Martin (L2)
- Pierre Bernard (L3)

**Matières:**
- MATH101 - Mathématiques Fondamentales (coef: 2.0)
- PHYS101 - Physique I (coef: 1.5)
- PROG101 - Introduction à la Programmation (coef: 2.0)

**Notes:** Générées pour chaque combinaison étudiant/matière

### Accéder à PostgreSQL:

```bash
# Depuis le conteneur
docker compose exec db psql -U grades_user -d grades_app

# Commandes utiles:
\dt                     # Lister les tables
\d grades_app_student   # Détail d'une table
SELECT * FROM grades_app_student;  # Voir les données
```

## 🔐 Sécurité et permissions

### Rôles disponibles:

1. **Admin** (is_staff)
   - Accès complet à l'API et admin
   - Tous les endpoints en lecture/écriture

2. **Enseignant** (groupe 'enseignant')
   - CRUD sur les étudiants
   - CRUD sur les matières
   - CRUD sur les notes

3. **Étudiant** (groupe 'etudiant')
   - Lecture seule sur leurs données
   - Pas d'accès aux données des autres

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
docker compose exec web pytest

# Tests unitaires uniquement
docker compose exec web pytest grades_app/tests/unit/

# Tests d'intégration uniquement
docker compose exec web pytest grades_app/tests/integration/

# Avec couverture
docker compose exec web pytest --cov=grades_app --cov-report=html

# Les rapports HTML sont dans: htmlcov/index.html
```

## 🐛 Dépannage

### L'app ne démarre pas

```bash
# Vérifier les logs
docker compose logs -f

# Vérifier que les ports ne sont pas utilisés
lsof -i :8000  # Django
lsof -i :5432  # PostgreSQL

# Nettoyer et recommencer
docker compose down -v
docker compose up --build
```

### Erreur de connexion à la BD

```bash
# La BD peut mettre 30-60 secondes à démarrer
# Le script attend jusqu'à 30 secondes
# Vérifier que la BD est prête:
docker compose logs db

# Redémarrer juste le conteneur web:
docker compose restart web
```

### Réinitialiser complètement

```bash
docker compose down -v
rm -rf postgres_data/  # Si volume local
docker system prune -a
docker compose up --build
```

## 📚 Structure complète

```
grades_app/
├── config/                 # Configuration Django
│   ├── settings.py        # Paramètres Django
│   ├── urls.py            # Routes principales
│   ├── wsgi.py
│   └── asgi.py
│
├── grades_app/            # Application Django
│   ├── api/              # API REST
│   │   ├── views.py      # ViewSets
│   │   ├── serializers.py # Sérialisateurs
│   │   ├── permissions.py # Permissions
│   │   └── urls.py       # Routes API
│   │
│   ├── migrations/        # Migrations DB
│   │   └── 0001_initial.py
│   │
│   ├── tests/            # Tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   │
│   ├── models.py         # Student, Subject, Grade
│   ├── services.py       # Logique métier
│   └── admin.py
│
├── scripts/              # Scripts utiles
│   └── seed.py          # Données de test
│
├── Dockerfile           # Image Docker
├── docker-compose.yml   # Orchestration
├── entrypoint.sh        # Script startup
├── Makefile            # Commandes
├── manage.py           # Django CLI
├── requirements.txt    # Dépendances Python
└── README.md           # Documentation
```

## ✨ Points clés

✅ **Production-ready**
- Conteneurisation complète
- Gestion des dépendances
- Migrations DB
- Permissions RBAC
- Tests complets

✅ **Développement facile**
- Hot reload du code
- Logs en direct
- Base de données persistente
- Données de test automatiques

✅ **Sécurisé**
- API avec authentification
- Permissions par rôle
- Validations au niveau des modèles
- Protection CSRF

---

**Questions?** Consultez:
- README.md pour la documentation complète
- docker-compose.yml pour la configuration
- Dockerfile pour le processus de build
- entrypoint.sh pour le startup
