# ✅ Grades App - Configuration Docker Complétée

## 🎉 Status: Application Opérationnelle

Votre application **Grades App** est maintenant **complètement fonctionnelle dans Docker** avec tous les services en cours d'exécution.

---

## 📊 Statut Actuel

```
✅ Base de données PostgreSQL       - Port: 5440
✅ Serveur Django                   - Port: 8888
✅ API REST                         - Opérationnelle
✅ Migrations appliquées            - 15 migrations Django
✅ Données de test                  - 3 étudiants, 3 matières, 9 notes
✅ Admin Django                     - Accessible
```

---

## 🚀 Comment Démarrer

### Option 1: Docker Compose (Recommandé)

```bash
cd /home/romuald/Downloads/grades_app
docker compose up -d    # Démarrer en arrière-plan
# ou
docker compose up       # Démarrer avec les logs visibles
```

### Option 2: Makefile

```bash
cd /home/romuald/Downloads/grades_app
make up                 # Démarrer
make logs               # Voir les logs
make down               # Arrêter
```

### Option 3: Script de démarrage

```bash
cd /home/romuald/Downloads/grades_app
./start.sh
```

---

## 🌐 Accès à l'Application

### API REST
- **URL**: http://localhost:8888/api/
- **Authentification**: Basic Auth
- **Utilisateur**: `admin`
- **Mot de passe**: `admin123`

### Admin Django
- **URL**: http://localhost:8888/admin/
- **Utilisateur**: `admin`
- **Mot de passe**: `admin123`

### Base de Données PostgreSQL
- **Host**: localhost
- **Port**: 5440
- **Database**: grades_app
- **Utilisateur**: grades_user
- **Mot de passe**: grades_pass

---

## 📡 Endpoints API

### Students (Étudiants)
```bash
# Lister les étudiants
curl -u admin:admin123 http://localhost:8888/api/students/

# Créer un étudiant
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alain","last_name":"Martin","level":"L1","email":"alain.martin@example.com"}' \
  http://localhost:8888/api/students/

# Détails d'un étudiant
curl -u admin:admin123 http://localhost:8888/api/students/1/

# Moyenne générale
curl -u admin:admin123 http://localhost:8888/api/students/1/average/
```

### Subjects (Matières)
```bash
# Lister les matières
curl -u admin:admin123 http://localhost:8888/api/subjects/

# Créer une matière
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"code":"ANG101","name":"Anglais","coefficient":1.5}' \
  http://localhost:8888/api/subjects/
```

### Grades (Notes)
```bash
# Lister les notes
curl -u admin:admin123 http://localhost:8888/api/grades/

# Créer une note
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"student":1,"subject":1,"value":15.5,"comment":"Bon travail"}' \
  http://localhost:8888/api/grades/
```

---

## 📋 Données Initiales

### Étudiants Créés
| ID | Prénom | Nom | Niveau | Email | Moyenne |
|----|--------|-----|--------|-------|---------|
| 1 | Jean | Dupont | L1 | jean.dupont@example.com | 12.53 |
| 2 | Marie | Martin | L2 | marie.martin@example.com | 17.32 |
| 3 | Pierre | Bernard | L3 | pierre.bernard@example.com | 15.94 |

### Matières Créées
| Code | Nom | Coefficient |
|------|-----|-------------|
| MATH101 | Mathématiques Fondamentales | 2.0 |
| PHYS101 | Physique I | 1.5 |
| PROG101 | Introduction à la Programmation | 2.0 |

---

## 🧪 Tests

### Lancer tous les tests
```bash
docker compose exec web pytest
```

### Tests unitaires uniquement
```bash
docker compose exec web pytest grades_app/tests/unit/
```

### Tests d'intégration
```bash
docker compose exec web pytest grades_app/tests/integration/
```

### Avec couverture de code
```bash
docker compose exec web pytest --cov=grades_app --cov-report=html
```

---

## 🔍 Vérifications et Maintenance

### Vérifier le statut des conteneurs
```bash
docker compose ps
```

### Voir les logs
```bash
# Tous les logs
docker compose logs -f

# Juste Django
docker compose logs -f web

# Juste PostgreSQL
docker compose logs -f db
```

### Accéder au shell Django
```bash
docker compose exec web python manage.py shell
```

### Accéder à PostgreSQL
```bash
docker compose exec db psql -U grades_user -d grades_app

# Lister les tables
\dt

# Voir les étudiants
SELECT * FROM grades_app_student;

# Voir les notes
SELECT * FROM grades_app_grade;
```

### Arrêter l'application
```bash
docker compose down
```

### Arrêter et nettoyer (supprimer les données)
```bash
docker compose down -v
```

---

## 🛠️ Structure de l'Application

```
grades_app/
├── config/
│   ├── settings.py           # Configuration Django
│   ├── urls.py              # Routes principales
│   └── ...
│
├── grades_app/
│   ├── api/
│   │   ├── views.py         # ViewSets REST
│   │   ├── serializers.py   # Sérialisateurs
│   │   ├── permissions.py   # Permissions RBAC
│   │   └── urls.py          # Routes API
│   │
│   ├── migrations/
│   │   └── 0001_initial.py  # Migration initiale
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   │
│   ├── models.py            # Student, Subject, Grade
│   ├── services.py          # Logique métier
│   └── admin.py
│
├── scripts/
│   └── seed.py              # Population de données
│
├── docker-compose.yml       # Orchestration Docker
├── Dockerfile              # Image Docker
├── entrypoint.sh           # Script de démarrage
├── Makefile                # Commandes utiles
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation
```

---

## 🔐 Rôles et Permissions

### Admin (is_staff)
- ✅ Accès complet à l'API
- ✅ Accès complet à l'admin Django
- ✅ CRUD sur tous les modèles

### Enseignant (groupe 'enseignant')
- ✅ CRUD sur les étudiants
- ✅ CRUD sur les matières
- ✅ CRUD sur les notes

### Étudiant (groupe 'etudiant')
- ✅ Lecture seule sur ses données
- ✅ Voir ses notes et sa moyenne
- ❌ Pas d'accès aux données d'autres étudiants

---

## 🐛 Dépannage

### Les ports ne répondent pas
```bash
# Vérifier que les conteneurs sont en cours d'exécution
docker compose ps

# Voir les erreurs
docker compose logs

# Redémarrer les conteneurs
docker compose restart
```

### Erreur: Port déjà utilisé
```bash
# Modifier docker-compose.yml ou utiliser des ports différents
# Les ports actuels sont:
# - API Django: 8888
# - PostgreSQL: 5440

# Ou arrêter l'autre conteneur
docker ps          # Trouver l'ID du conteneur
docker stop <id>   # L'arrêter
```

### Réinitialiser la base de données
```bash
docker compose down -v
docker compose up --build
```

### Accès shell Django pour debugging
```bash
docker compose exec web python manage.py shell

# Dans le shell:
from grades_app.models import Student
student = Student.objects.first()
print(student.compute_general_average())
```

---

## 📚 Documentation Complète

Pour plus de détails:
- **README.md** - Documentation générale
- **DOCKER_QUICKSTART.md** - Guide de démarrage Docker
- **Makefile** - Commandes disponibles
- **docker-compose.yml** - Configuration des services
- **Dockerfile** - Processus de construction

---

## ✨ Points Clés

✅ **Production-ready**
- Docker Compose entièrement configuré
- Migrations de base de données gérées
- Gestion des dépendances
- Healthchecks configurés

✅ **Développement Facile**
- Hot reload du code
- Logs en direct visibles
- Base de données persistante
- Données de test automatiques
- Makefile pour commandes rapides

✅ **Sécurisé**
- API avec authentification
- Permissions par rôle
- Validations au niveau des modèles
- Protection CSRF

✅ **Testé et Validé**
- 3 étudiants créés
- 3 matières créées
- 9 notes générées
- API opérationnelle et testée
- Admin Django accessible

---

## 📞 Commandes Rapides

```bash
# Démarrer
docker compose up -d

# Arrêter
docker compose down

# Voir les logs
docker compose logs -f

# Lancer les tests
docker compose exec web pytest

# Accéder au shell Django
docker compose exec web python manage.py shell

# Nettoyage complet
docker compose down -v && rm -rf postgres_data
```

---

**🎯 Votre application est maintenant prête à être utilisée!**

Pour questions, consultez la documentation ou vérifiez les logs avec `docker compose logs`.
