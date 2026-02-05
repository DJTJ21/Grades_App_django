#!/bin/bash

# Script pour lancer l'application Grades App avec Docker Compose

set -e

echo "================================"
echo "  Grades App - Docker Launcher"
echo "================================"
echo ""

# Vérifier que docker et docker-compose sont installés
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

echo "✅ Docker et Docker Compose trouvés"
echo ""

# Construire et démarrer les conteneurs
echo "🚀 Construction et démarrage des conteneurs..."
docker-compose up --build

echo ""
echo "✅ Application lancée!"
echo ""
echo "📋 Accès:"
echo "   - API: http://localhost:8000/api/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - Base de données: localhost:5432"
echo ""
echo "👤 Identifiants admin:"
echo "   - Utilisateur: admin"
echo "   - Mot de passe: admin123"
echo ""
echo "Pour arrêter: Appuyez sur Ctrl+C"
