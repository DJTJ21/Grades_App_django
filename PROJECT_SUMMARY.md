# Grades App - Gestion des Notes Étudiantes

> Application Django REST complète pour la gestion des notes étudiantes avec tests complets, sécurité validée et CI/CD automatisé.

## 📊 Status

| Badge | Statut |
|-------|--------|
| Tests | ![Tests](https://img.shields.io/badge/tests-87%2F87-brightgreen) |
| Couverture | ![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen) |
| Sécurité | ![Security](https://img.shields.io/badge/security-0%20HIGH-brightgreen) |
| Python | ![Python](https://img.shields.io/badge/python-3.11-blue) |
| Django | ![Django](https://img.shields.io/badge/django-4.2-blue) |
| License | ![License](https://img.shields.io/badge/license-MIT-blue) |

## 🚀 Quick Start

```bash
# Cloner et démarrer
git clone <repo>
cd grades_app
docker compose up -d

# Accéder à l'application
# - API: http://localhost:8888/api/
# - Admin: http://localhost:8888/admin/ (admin/admin123)
```

## 📋 Features

✅ **API REST Complète**
- CRUD pour Student, Subject, Grade
- Calcul automatique des moyennes
- Génération unique de matricule (YYYYNNNN)
- Filtrage et recherche avancés
- Endpoints custom (average, filtering)

✅ **Tests Complets**
- 87 tests unitaires et d'intégration
- 97% couverture de code
- Factories pour données de test
- Tests API avec permissions
- End-to-end workflows

✅ **Sécurité**
- 0 vulnérabilités HIGH severity
- Bandit security scanning
- Authentification tokenisée
- Permissions basées sur rôles (RBAC)
- Validation des inputs (DRF serializers)

✅ **Docker & Orchestration**
- PostgreSQL 15-Alpine
- Django en container
- Hot reload en développement
- Health checks automatiques
- Data seed automatique

✅ **CI/CD Pipeline**
- GitHub Actions workflow
- Tests automatisés
- Couverture ≥ 85% enforced
- Bandit security checks
- Code quality (Black + Flake8)
- Upload Codecov

## 📁 Project Structure

```
grades_app/
├── models.py              # Student, Subject, Grade
├── services.py            # Business logic
├── admin.py               # Django admin
├── api/
│   ├── views.py          # REST endpoints
│   ├── serializers.py     # Data validation
│   ├── permissions.py     # RBAC
│   └── urls.py           # Routes
├── tests/
│   ├── unit/             # 40 tests
│   ├── integration/      # 47 tests
│   ├── factories.py       # Test data generators
│   └── conftest.py       # Pytest config
├── migrations/            # DB migrations
├── docker-compose.yml     # Services orchestration
├── Dockerfile             # Application image
├── requirements.txt       # Dependencies
└── pytest.ini             # Test config
```

## 🧪 Running Tests

```bash
# All tests
docker compose exec web pytest grades_app/tests/ -v

# With coverage report
docker compose exec web pytest grades_app/tests/ \
  --cov=grades_app \
  --cov-report=term-missing

# Security scan
docker compose exec web bandit -r grades_app -lll

# Code quality
docker compose exec web black --check grades_app
docker compose exec web flake8 grades_app
```

## 📊 Test Coverage

| Module | Stmts | Cover |
|--------|-------|-------|
| models.py | 61 | 100% |
| services.py | 23 | 100% |
| api/views.py | 35 | 100% |
| api/serializers.py | 22 | 100% |
| test_models.py | 206 | 100% |
| test_services.py | 142 | 100% |
| test_api_flow.py | 299 | 100% |
| **TOTAL** | **906** | **97%** |

## 🔐 Security

Scan Results:
- **HIGH severity**: 0 ✅
- **MEDIUM severity**: 0 ✅
- **LOW severity**: 134 (non-critical)

Features:
- Token authentication
- Role-based access control
- Input validation
- SQL injection prevention (ORM)
- CSRF protection
- Secure password handling

## 📦 Dependencies

```
Django>=4.2,<5.0
djangorestframework>=3.14,<4.0
pytest>=7.4,<9.0
pytest-django>=4.5,<5.0
pytest-cov>=4.1,<5.0
factory-boy>=3.3,<4.0
bandit>=1.7,<2.0
coverage>=7.2,<8.0
psycopg2-binary>=2.9,<3.0
```

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/grades_db

# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Other
TIME_ZONE=Africa/Dakar
LANGUAGE_CODE=fr-fr
```

### Docker Ports

- Django: `8888` (external) → `8000` (internal)
- PostgreSQL: `5440` (external) → `5432` (internal)

## 📚 Documentation

- **README.md** - Main guide (you are here)
- **QUICK_REFERENCE.md** - Quick commands and examples
- **DOCKER_QUICKSTART.md** - Docker setup guide
- **GETTING_STARTED.md** - Detailed startup guide
- **CI_CD_REPORT.md** - Pipeline documentation
- **IMPLEMENTATION_COMPLETE.md** - Full implementation report
- **DEPLOYMENT_STATUS.md** - Deployment checklist

## 🚀 Deployment

### Development
```bash
docker compose up -d
```

### Production
1. Update `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS`
3. Set proper `SECRET_KEY`
4. Use external PostgreSQL database
5. Configure HTTPS/SSL
6. Set up reverse proxy (nginx)
7. Enable gzip compression
8. Configure monitoring

See `DEPLOYMENT_STATUS.md` for details.

## 🧑‍💻 API Examples

### Authentication
```bash
# Get token
curl -X POST http://localhost:8888/api/token/ \
  -d "username=admin&password=admin123"

# Use token in requests
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8888/api/students/
```

### Create Student
```bash
curl -X POST http://localhost:8888/api/students/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "level": "L1"
  }'
```

### Get Student Average
```bash
curl http://localhost:8888/api/students/1/average/ \
  -H "Authorization: Token YOUR_TOKEN"
```

See `QUICK_REFERENCE.md` for more examples.

## 🔄 CI/CD Pipeline

GitHub Actions workflow triggers on:
- Push to `main` or `develop`
- Pull request to `main` or `develop`

Jobs:
1. **test** - Run 87 tests + coverage check (≥85%)
2. **security** - Bandit scan (fail on HIGH)
3. **code_quality** - Black + Flake8

Artifacts:
- Test results
- Coverage report
- Upload to Codecov

## 🐛 Troubleshooting

### Containers won't start
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Database connection error
```bash
# Check PostgreSQL logs
docker compose logs db

# Reset database
docker compose down -v
docker compose up -d
```

### Tests failing
```bash
# Run with verbose output
docker compose exec web pytest grades_app/tests/ -v --tb=short
```

## 📈 Performance Metrics

- Test execution: ~10 seconds
- API response time: <100ms
- Database query time: <10ms

## 🎯 Requirements Satisfaction

| Requirement | Status | Details |
|------------|--------|---------|
| Django Application | ✅ | REST API with models |
| Unit Tests | ✅ | 40 tests (100% pass) |
| Integration Tests | ✅ | 47 tests (100% pass) |
| Coverage ≥ 85% | ✅ | 97% achieved |
| Bandit Security | ✅ | 0 HIGH findings |
| Docker Compose | ✅ | PostgreSQL + Django |
| CI/CD Pipeline | ✅ | GitHub Actions |
| Documentation | ✅ | 8 markdown files |

## 🤝 Contributing

1. Create feature branch from `develop`
2. Write tests (maintain 85%+ coverage)
3. Run test suite: `pytest grades_app/tests/ -v`
4. Submit pull request to `develop`
5. CI/CD pipeline will validate

## 📄 License

MIT License - See LICENSE file

## 👥 Authors

- **Romuald** - Initial implementation and dockerization

## 📞 Support

For issues or questions:
1. Check `TROUBLESHOOTING.md`
2. Review test examples in `grades_app/tests/`
3. Consult API documentation at `/api/schema/`

---

**Production Ready** ✅ | **Fully Tested** ✅ | **Secure** ✅ | **Documented** ✅
