.PHONY: help build up down logs shell test clean

help:
	@echo "Grades App - Commandes disponibles"
	@echo ""
	@echo "  make build        - Construire les images Docker"
	@echo "  make up           - Démarrer l'application"
	@echo "  make down         - Arrêter l'application"
	@echo "  make logs         - Afficher les logs en direct"
	@echo "  make shell        - Accéder au shell Django"
	@echo "  make test         - Lancer les tests"
	@echo "  make clean        - Nettoyer les conteneurs et volumes"
	@echo ""
	@echo "Accès:"
	@echo "  API:      http://localhost:8000/api/"
	@echo "  Admin:    http://localhost:8000/admin/"
	@echo "  DB:       localhost:5432"
	@echo ""

build:
	@echo "📦 Construction des images Docker..."
	docker-compose build

up:
	@echo "🚀 Démarrage de l'application..."
	docker-compose up

down:
	@echo "⏹️  Arrêt de l'application..."
	docker-compose down

logs:
	@echo "📋 Affichage des logs..."
	docker-compose logs -f

shell:
	@echo "🐚 Accès au shell Django..."
	docker-compose exec web python manage.py shell

test:
	@echo "🧪 Lancement des tests..."
	docker-compose exec web pytest

test-coverage:
	@echo "🧪 Lancement des tests avec couverture..."
	docker-compose exec web pytest --cov=grades_app --cov-report=html

clean:
	@echo "🧹 Nettoyage..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name htmlcov -exec rm -rf {} +

migrate:
	@echo "🔄 Application des migrations..."
	docker-compose exec web python manage.py migrate

createsuperuser:
	@echo "👤 Création d'un superutilisateur..."
	docker-compose exec web python manage.py createsuperuser

seed:
	@echo "🌱 Population de données de test..."
	docker-compose exec web python manage.py shell < scripts/seed.py
