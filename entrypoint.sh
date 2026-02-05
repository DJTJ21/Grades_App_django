#!/bin/bash

set -e

echo "========================================="
echo "  Grades App - Docker Startup"
echo "========================================="
echo ""

# Attendre que la base de données soit prête
echo "⏳ Vérification de la base de données..."
for i in {1..30}; do
    if nc -z "$DJANGO_DB_HOST" "$DJANGO_DB_PORT" 2>/dev/null; then
        echo "✅ Base de données disponible"
        break
    fi
    echo "  Tentative $i/30..."
    sleep 1
done

if ! nc -z "$DJANGO_DB_HOST" "$DJANGO_DB_PORT" 2>/dev/null; then
    echo "❌ Impossible de se connecter à la base de données après 30 secondes"
    exit 1
fi

echo ""
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo ""
echo "👤 Configuration des groupes et utilisateurs..."
python manage.py shell << 'DJANGO_SHELL'
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model

# Créer les groupes
enseignant_group, created = Group.objects.get_or_create(name='enseignant')
etudiant_group, created = Group.objects.get_or_create(name='etudiant')
print("✓ Groupes créés")

# Créer le superutilisateur
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Superutilisateur 'admin' créé (mot de passe: admin123)")
else:
    print("✓ Superutilisateur 'admin' existe déjà")

# Créer des données exemple
from grades_app.models import Student, Subject, Grade
from django.utils import timezone

if not Student.objects.exists():
    print("\n🌱 Création des données de test...")
    
    # Créer des étudiants
    students = [
        Student.objects.create(
            first_name='Jean',
            last_name='Dupont',
            level='L1',
            email='jean.dupont@example.com'
        ),
        Student.objects.create(
            first_name='Marie',
            last_name='Martin',
            level='L2',
            email='marie.martin@example.com'
        ),
        Student.objects.create(
            first_name='Pierre',
            last_name='Bernard',
            level='L3',
            email='pierre.bernard@example.com'
        ),
    ]
    print(f"✓ {len(students)} étudiants créés")
    
    # Créer des matières
    subjects = [
        Subject.objects.create(
            code='MATH101',
            name='Mathématiques Fondamentales',
            coefficient=2.0
        ),
        Subject.objects.create(
            code='PHYS101',
            name='Physique I',
            coefficient=1.5
        ),
        Subject.objects.create(
            code='PROG101',
            name='Introduction à la Programmation',
            coefficient=2.0
        ),
    ]
    print(f"✓ {len(subjects)} matières créées")
    
    # Créer des notes
    grade_count = 0
    for student in students:
        for subject in subjects:
            Grade.objects.create(
                student=student,
                subject=subject,
                value=10.0 + (hash(f"{student.id}{subject.id}") % 100) / 10,
                date=timezone.now().date(),
                comment='Note initiale'
            )
            grade_count += 1
    print(f"✓ {grade_count} notes créées")
    print("\n✅ Données de test chargées avec succès!")
else:
    print("✓ Les données existent déjà")

print("\n✅ Configuration terminée!")
DJANGO_SHELL

echo ""
echo "========================================="
echo "  🚀 Démarrage du serveur Django"
echo "========================================="
echo ""
echo "📋 Accès à l'application:"
echo "   - API:       http://localhost:8000/api/"
echo "   - Admin:     http://localhost:8000/admin/"
echo "   - DB:        localhost:5432"
echo ""
echo "👤 Identifiants:"
echo "   - Utilisateur: admin"
echo "   - Mot de passe: admin123"
echo ""

# Démarrer le serveur Django
python manage.py runserver 0.0.0.0:8000
