# Quick Reference - Grades App

## 🚀 5 Secondes pour Démarrer

```bash
cd /home/romuald/Downloads/grades_app
docker compose up -d
```

Puis ouvrez:
- 🌐 API: http://localhost:8888/api/
- 🔐 Admin: http://localhost:8888/admin/ (admin/admin123)

## 📊 Vérifier les Tests

```bash
# Tous les tests
docker compose exec web pytest grades_app/tests/ -v

# Avec couverture
docker compose exec web pytest grades_app/tests/ --cov=grades_app --cov-report=term-missing

# Sécurité
docker compose exec web bandit -r grades_app -lll
```

## 📁 Structure du Projet

```
grades_app/
├── models.py              ← Student, Subject, Grade
├── services.py            ← Logique métier
├── admin.py               ← Interface Django
├── api/
│   ├── views.py          ← API REST endpoints
│   ├── serializers.py     ← Data validation
│   ├── permissions.py     ← RBAC
│   └── urls.py           ← Routes API
├── tests/
│   ├── unit/
│   │   ├── test_models.py       (20 tests)
│   │   └── test_services.py     (20 tests)
│   ├── integration/
│   │   └── test_api_flow.py     (47 tests)
│   ├── factories.py             ← Test data
│   └── conftest.py              ← Pytest config
└── migrations/            ← Database migrations
```

## 📈 Statistiques

| Métrique | Valeur | Objectif | Statut |
|----------|--------|----------|--------|
| Tests | 87 | - | ✅ 100% pass |
| Couverture | 97% | 85% | ✅ +12% |
| Sécurité HIGH | 0 | 0 | ✅ OK |
| LOC | 906 | - | ✅ OK |

## 🔧 Fichiers Importants

| Fichier | Purpose |
|---------|---------|
| `docker-compose.yml` | Orchestration services |
| `Dockerfile` | Image Django |
| `requirements.txt` | Dépendances Python |
| `.github/workflows/tests.yml` | CI/CD Pipeline |
| `pytest.ini` | Configuration pytest |
| `manage.py` | CLI Django |

## 🧪 Exemples API

### Créer un étudiant
```bash
curl -X POST http://localhost:8888/api/students/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"first_name": "Jean", "last_name": "Dupont", "email": "jean@example.com", "level": "L1"}'
```

### Lister les étudiants
```bash
curl http://localhost:8888/api/students/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Créer une matière
```bash
curl -X POST http://localhost:8888/api/subjects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"code": "MATH101", "name": "Mathématiques", "coefficient": 2.0}'
```

### Assigner une note
```bash
curl -X POST http://localhost:8888/api/grades/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"student": 1, "subject": 1, "value": 15.5, "comment": "Bon travail"}'
```

### Obtenir la moyenne d'un étudiant
```bash
curl http://localhost:8888/api/students/1/average/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## 🔐 Authentification

1. **Créer un utilisateur:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

2. **Obtenir un token:**
   ```bash
   curl -X POST http://localhost:8888/api/token/ \
     -d "username=admin&password=admin123"
   ```

3. **Utiliser le token:**
   ```bash
   curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8888/api/
   ```

## 🛑 Arrêter l'Application

```bash
docker compose down -v  # with volume cleanup
# ou
docker compose down     # keep volumes
```

## 📚 Documentation Complète

- `README.md` - Guide principal
- `DOCKER_QUICKSTART.md` - Quick start Docker
- `GETTING_STARTED.md` - Démarrage détaillé
- `CI_CD_REPORT.md` - Pipeline CI/CD
- `IMPLEMENTATION_COMPLETE.md` - Rapport final
- `DEPLOYMENT_STATUS.md` - Statut déploiement
- `MODIFICATIONS_SUMMARY.md` - Changelog

## 🐛 Dépannage

### Les containers ne démarrent pas
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
sleep 15  # Wait for initialization
```

### Tests qui échouent
```bash
docker compose exec web pytest grades_app/tests/ -v --tb=short
```

### Accès à la DB directement
```bash
docker compose exec db psql -U postgres -d grades_db
```

### Logs du serveur
```bash
docker compose logs -f web
```

## 💡 Pro Tips

1. **Hot reload activé** - Modifiez le code et les changements se rechargeront automatiquement
2. **Seed data automatique** - 3 étudiants et 3 matières créées au démarrage
3. **Migrations automatiques** - Le entrypoint.sh lance `manage.py migrate`
4. **Admin Django** - http://localhost:8888/admin/ pour gérer les données
5. **API auto-documentée** - Utilisez l'interface DRF browsable à /api/

## 🚀 Pour la Production

1. Changer `DEBUG=False` dans `settings.py`
2. Configurer `ALLOWED_HOSTS`
3. Utiliser une vraie base de données externalisée
4. Configurer le secret key
5. Activer HTTPS
6. Configurer un reverse proxy (nginx)
7. Activer la compression gzip
8. Mettre en place le monitoring

---

**L'application est 100% fonctionnelle et prête à l'emploi! 🎉**
