#!/bin/bash

# Script de vérification de l'application

echo "========================================"
echo "  Grades App - Vérification"
echo "========================================"
echo ""

# Vérifier que Docker et docker-compose sont installés
echo "🔍 Vérification des prérequis..."
docker --version > /dev/null 2>&1 && echo "✅ Docker installé" || echo "❌ Docker non installé"
docker compose version > /dev/null 2>&1 && echo "✅ Docker Compose installé" || echo "❌ Docker Compose non installé"
echo ""

# Vérifier l'état des conteneurs
echo "🔍 État des conteneurs..."
docker compose ps
echo ""

# Tester l'API
echo "🔍 Test de l'API..."
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -u admin:admin123 http://localhost:8888/api/)
if [ "$API_RESPONSE" = "200" ]; then
    echo "✅ API accessible (HTTP $API_RESPONSE)"
else
    echo "⚠️  API retourne le code $API_RESPONSE"
fi
echo ""

# Tester les endpoints principaux
echo "🔍 Test des endpoints..."
echo "   Students:  $(curl -s -u admin:admin123 -o /dev/null -w '%{http_code}' http://localhost:8888/api/students/)"
echo "   Subjects:  $(curl -s -u admin:admin123 -o /dev/null -w '%{http_code}' http://localhost:8888/api/subjects/)"
echo "   Grades:    $(curl -s -u admin:admin123 -o /dev/null -w '%{http_code}' http://localhost:8888/api/grades/)"
echo ""

# Compter les données
echo "📊 Données en base de données:"
STUDENTS=$(curl -s -u admin:admin123 http://localhost:8888/api/students/ | grep -o '"id"' | wc -l)
SUBJECTS=$(curl -s -u admin:admin123 http://localhost:8888/api/subjects/ | grep -o '"id"' | wc -l)
GRADES=$(curl -s -u admin:admin123 http://localhost:8888/api/grades/ | grep -o '"id"' | wc -l)
echo "   Students: $STUDENTS"
echo "   Subjects: $SUBJECTS"
echo "   Grades:   $GRADES"
echo ""

echo "========================================"
echo "  ✅ Vérification terminée"
echo "========================================"
echo ""
echo "📋 Accès:"
echo "   API:   http://localhost:8888/api/"
echo "   Admin: http://localhost:8888/admin/"
echo "   DB:    localhost:5440"
echo ""
echo "👤 Identifiants: admin / admin123"
echo ""
