# 📊 Guide de Présentation - Grades App

## 🎯 Vue d'Ensemble (3 minutes)

### Qu'est-ce que c'est?

**Grades App** est une **application web de gestion des notes étudiantes** construite avec Django et PostgreSQL.

Elle permet aux établissements d'enseignement de:
- ✅ Gérer les étudiants (inscription, niveau d'études)
- ✅ Gérer les matières (codes, noms, coefficients)
- ✅ Attribuer les notes aux étudiants
- ✅ Calculer les moyennes générales
- ✅ Générer des matricules uniques automatiquement

### Qui l'utilise?

- 👨‍💼 **Administrateurs** - Gestion complète
- 👨‍🏫 **Enseignants** - Attribution des notes
- 👨‍🎓 **Étudiants** - Consultation des notes

---

## 📚 Concepts Clés Expliqués

### 1. **Qu'est-ce qu'un Grade (Note)?**

Un **Grade** représente la **note obtenue par un étudiant dans une matière à une date donnée**.

```
Grade = Note d'un étudiant dans une matière
┌─────────────────────────────────────────────┐
│ Étudiant: Jean Dupont (Matricule: 20260001) │
│ Matière:  Mathématiques (MATH101)           │
│ Note:     15.5/20                           │
│ Date:     2026-02-05                        │
│ Coefficient: 2.0                            │
└─────────────────────────────────────────────┘
```

**Important:** Un étudiant peut avoir **plusieurs notes** dans la même matière (à des dates différentes):
- Test 1: 12/20 (le 2026-01-15)
- Test 2: 18/20 (le 2026-02-05)
- Examen Final: 16/20 (le 2026-03-10)

La **moyenne générale** est le **produit pondéré** de toutes les notes par les coefficients.

### 2. **Qu'est-ce qu'un Matricule?**

Un **Matricule** est un **identifiant unique automatique** généré pour chaque étudiant au format:

```
YYYYNNNN
│    └─ Numéro séquentiel (0001, 0002, 0003...)
└────── Année d'inscription (2026)

Exemples:
  20260001 - Première inscription en 2026
  20260002 - Deuxième inscription en 2026
  20260003 - Troisième inscription en 2026
  20270001 - Première inscription en 2027
```

**Avantage:** Chaque étudiant a un ID **unique et irrévocable** sans intervention manuelle.

### 3. **Qu'est-ce qu'un Coefficient?**

Un **Coefficient** représente **l'importance relative d'une matière** dans le calcul de la moyenne.

```
Matière             │ Note │ Coefficient │ Pondération
───────────────────┼──────┼─────────────┼──────────────
Mathématiques       │  15  │     2.0     │  15 × 2 = 30
Physique            │  14  │     1.5     │  14 × 1.5 = 21
Programmation       │  16  │     2.0     │  16 × 2 = 32
───────────────────┼──────┼─────────────┼──────────────
Moyenne = (30 + 21 + 32) / (2 + 1.5 + 2) = 83 / 5.5 = 15.09
```

**Calcul:** `Moyenne = Σ(Note × Coefficient) / Σ(Coefficients)`

---

## 🏗️ Architecture Technique (2 minutes)

```
┌─────────────────────────────────────────────┐
│         Client (Navigateur)                 │
│  http://localhost:8888/api/                 │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │   Django REST API   │
        │  (Python 4.2.28)    │
        ├─────────────────────┤
        │ • Students          │
        │ • Subjects          │
        │ • Grades            │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  PostgreSQL 15      │
        │  (Base de données)  │
        └─────────────────────┘
```

**Stack Technologique:**
- **Backend:** Django 4.2.28 + Django REST Framework
- **Database:** PostgreSQL 15-Alpine
- **Containerization:** Docker + Docker Compose
- **Testing:** pytest + factory-boy (87 tests)
- **Security:** Bandit (0 HIGH severity)

---

## 🚀 Démarrage de l'Application

### Étape 1: Démarrer les containers Docker

```bash
cd /home/romuald/Downloads/grades_app
docker compose up -d
```

**Attendre ~15 secondes** pour que PostgreSQL démarre et les migrations s'appliquent.

### Étape 2: Vérifier le démarrage

```bash
docker compose ps
```

**Résultat attendu:**
```
NAME              STATUS              PORTS
grades_app_db     Up (healthy)        0.0.0.0:5440->5432/tcp
grades_app_web    Up (running)        0.0.0.0:8888->8000/tcp
```

### Étape 3: Accéder à l'application

- **API REST:** http://localhost:8888/api/
- **Admin Django:** http://localhost:8888/admin/
- **Credentials:** `admin` / `admin123`

---

## 📋 Tests Manuels (Étape par Étape)

### TEST 1: Création Automatique de Matricule

**Objectif:** Démontrer que le matricule est généré **automatiquement** et **uniquement**.

**Étapes:**

1. Ouvrir l'admin: http://localhost:8888/admin/
2. Connexion: `admin` / `admin123`
3. Aller à **Students**
4. Cliquer **"Add Student"**
5. Remplir le formulaire:
   - First name: `Jean`
   - Last name: `Dupont`
   - Email: `jean@example.com`
   - Level: `L1`
   - **Laisser "Matricule" VIDE** (ne rien écrire!)
6. Cliquer **"Save"**

**Résultat Attendu:**
```
Student "Jean Dupont (20260001)" was added successfully.
```

Le matricule **20260001** a été généré automatiquement! ✅

**Explication:**
- **2026** = Année actuelle
- **0001** = Numéro séquentiel auto-incrémenté

---

### TEST 2: Unicité du Matricule

**Objectif:** Vérifier que chaque matricule est **unique** et que le **numéro séquentiel s'incrémente**.

**Étapes:**

1. Ajouter un **deuxième étudiant**:
   - First name: `Marie`
   - Last name: `Martin`
   - Email: `marie@example.com`
   - Level: `L2`
   - Matricule: **VIDE**
2. Cliquer **"Save"**

**Résultat Attendu:**
```
Student "Marie Martin (20260002)" was added successfully.
```

Le matricule est **20260002** (incrémenté automatiquement) ✅

**Explication:**
- Chaque nouveau student a un numéro +1
- Impossible d'avoir deux étudiants avec le même matricule

---

### TEST 3: Création d'une Matière

**Objectif:** Ajouter une matière qui sera utilisée pour les notes.

**Étapes:**

1. Dans l'admin, aller à **Subjects**
2. Cliquer **"Add Subject"**
3. Remplir:
   - Code: `MATH101` (identifiant unique)
   - Name: `Mathématiques Fondamentales`
   - Coefficient: `2.0` (importance de la matière)
4. Cliquer **"Save"**

**Résultat Attendu:**
```
Subject "MATH101 - Mathématiques Fondamentales" was added successfully.
```

**Explication:**
- Le coefficient `2.0` signifie que cette matière compte **2× plus** dans la moyenne qu'une matière de coefficient 1.0

---

### TEST 4: Attribuer une Note (Grade)

**Objectif:** Assigner une note à un étudiant dans une matière.

**Étapes:**

1. Dans l'admin, aller à **Grades**
2. Cliquer **"Add Grade"**
3. Remplir:
   - Student: `Jean Dupont (20260001)`
   - Subject: `MATH101 - Mathématiques Fondamentales`
   - Value: `15.5` (la note sur 20)
   - Date: `2026-02-05` (date de l'évaluation)
   - Comment: `Bon travail` (optionnel)
4. Cliquer **"Save"**

**Résultat Attendu:**
```
Grade "20260001 - MATH101: 15.5" was added successfully.
```

**Explication:**
- La note **15.5/20** a été enregistrée pour Jean Dupont
- Cette note sera utilisée pour calculer sa moyenne générale

---

### TEST 5: Validation des Notes (Limites 0-20)

**Objectif:** Vérifier que seules les notes entre **0 et 20** sont acceptées.

**Étapes:**

1. Essayer d'ajouter une note invalide:
   - Value: `25` (plus grand que 20)
2. Cliquer **"Save"**

**Résultat Attendu:**
```
❌ ERROR: Grade must be between 0 and 20.
```

La validation **rejette automatiquement** les notes invalides! ✅

**Essayer aussi:**
- Value: `-5` → Rejeté ❌
- Value: `20` → Accepté ✅
- Value: `0` → Accepté ✅

---

### TEST 6: Calcul Automatique de la Moyenne Générale

**Objectif:** Démontrer que la moyenne se calcule **automatiquement** avec les coefficients.

**Étapes:**

1. Ajouter 3 matières:
   ```
   MATH101 - Mathématiques        (coef: 2.0)
   PHYS101 - Physique              (coef: 1.5)
   PROG101 - Programmation         (coef: 2.0)
   ```

2. Assigner les notes à Jean Dupont:
   ```
   MATH101: 15 (15 × 2.0 = 30)
   PHYS101: 14 (14 × 1.5 = 21)
   PROG101: 16 (16 × 2.0 = 32)
   ```

3. Aller dans l'admin Students
4. Cliquer sur **Jean Dupont (20260001)**
5. **Regarder le champ "General Average"**

**Résultat Attendu:**
```
General Average: 15.09

Calcul: (30 + 21 + 32) / (2.0 + 1.5 + 2.0)
      = 83 / 5.5
      = 15.09
```

La moyenne se calcule **automatiquement** avec la formule pondérée! ✅

---

### TEST 7: Unicité (Student, Subject, Date)

**Objectif:** Vérifier qu'un étudiant ne peut avoir qu'**une seule note** pour une matière à une date donnée.

**Étapes:**

1. Essayer d'ajouter une **deuxième note** à Jean Dupont:
   - Student: `Jean Dupont (20260001)`
   - Subject: `MATH101`
   - Value: `18`
   - Date: `2026-02-05` (MÊME DATE!)

2. Cliquer **"Save"**

**Résultat Attendu:**
```
❌ ERROR: Grade with this Student, Subject and Date already exists.
```

Le système empêche les **doublons**! ✅

**Mais si on change la date:**
- Date: `2026-02-10` (date différente)
- Cliquer **"Save"**

**Résultat Attendu:**
```
✅ Grade "20260001 - MATH101: 18" was added successfully.
```

**Explication:**
- Même matière, même étudiant = OK si **date différente**
- Permet plusieurs tests/exams dans la même matière

---

### TEST 8: API REST - Lister les Étudiants

**Objectif:** Montrer que l'API REST fonctionne et retourne les données en JSON.

**Étapes:**

1. Ouvrir un terminal:
   ```bash
   curl -u admin:admin123 http://localhost:8888/api/students/
   ```

**Résultat Attendu:**
```json
[
  {
    "id": 1,
    "matricule": "20260001",
    "first_name": "Jean",
    "last_name": "Dupont",
    "level": "L1",
    "email": "jean@example.com",
    "general_average": 15.09
  },
  {
    "id": 2,
    "matricule": "20260002",
    "first_name": "Marie",
    "last_name": "Martin",
    "level": "L2",
    "email": "marie@example.com",
    "general_average": 0.0
  }
]
```

**Explication:**
- L'API retourne les données en **JSON**
- La moyenne générale est calculée automatiquement
- Marie n'a pas de notes, donc moyenne = 0

---

### TEST 9: API REST - Créer un Étudiant via API

**Objectif:** Créer un étudiant directement via l'API (sans interface web).

**Étapes:**

```bash
curl -X POST http://localhost:8888/api/students/ \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "first_name": "Pierre",
    "last_name": "Bernard",
    "email": "pierre@example.com",
    "level": "L3"
  }'
```

**Résultat Attendu:**
```json
{
  "id": 3,
  "matricule": "20260003",
  "first_name": "Pierre",
  "last_name": "Bernard",
  "level": "L3",
  "email": "pierre@example.com",
  "general_average": 0.0
}
```

Le matricule **20260003** a été généré automatiquement! ✅

---

### TEST 10: Moyenne Générale d'un Étudiant via API

**Objectif:** Récupérer la moyenne générale via l'API.

**Étapes:**

```bash
curl -u admin:admin123 http://localhost:8888/api/students/1/average/
```

**Résultat Attendu:**
```json
{
  "matricule": "20260001",
  "first_name": "Jean",
  "last_name": "Dupont",
  "general_average": 15.09
}
```

---

## 🧪 Tests Automatisés

L'application contient **87 tests automatiques**:

```bash
docker compose exec web pytest grades_app/tests/ -v
```

**Résultat:**
```
✅ 87 passed in 10.83s
```

### Distribution des Tests:

| Catégorie | Nombre | Rôle |
|-----------|--------|------|
| **Tests Modèles** | 20 | Valider Student, Subject, Grade |
| **Tests Services** | 20 | Valider matricule, validation, moyennes |
| **Tests API** | 47 | Valider les endpoints REST |

### Couverture:

```
Total Couverture: 97% (objectif: 85%)

✅ models.py:     100% couvert
✅ services.py:   100% couvert
✅ api/views.py:  100% couvert
```

---

## 🔐 Sécurité

### Scan Bandit (Sécurité):

```bash
docker compose exec web bandit -r grades_app -lll
```

**Résultat:**
```
❌ HIGH severity findings:    0 ✅
❌ MEDIUM severity findings:  0 ✅
⚠️  LOW severity findings:    134 (non-critiques)
```

**Application Sécurisée!** ✅

---

## 📊 Résumé des Points Clés

### Qu'est-ce qu'un Grade?
- Une **note** attribuée à un étudiant dans une matière
- Entre **0 et 20**
- À une **date spécifique**
- Avec un **coefficient** (importance)

### Qu'est-ce qu'un Matricule?
- **YYYYNNNN** (année + numéro séquentiel)
- **Généré automatiquement** (pas d'intervention manuelle)
- **Unique** pour chaque étudiant
- Exemple: `20260001` (1er étudiant inscrit en 2026)

### Qu'est-ce qu'un Coefficient?
- **Poids** d'une matière dans la moyenne
- Permet de valoriser certaines matières
- Calcul: `Moyenne = Σ(Note × Coefficient) / Σ(Coefficients)`

### Qu'est-ce que la Moyenne Générale?
- **Moyenne pondérée** de tous les notes
- Tient compte des coefficients
- Se calcule **automatiquement**
- Mise à jour chaque fois qu'une note est ajoutée

---

## 💡 Points à Souligner

1. ✅ **Automatisation:** Matricule généré sans intervention
2. ✅ **Validation:** Les notes doivent être entre 0 et 20
3. ✅ **Intégrité:** Impossible d'avoir deux notes identiques à la même date
4. ✅ **Calcul Intelligent:** Les moyennes se mettent à jour automatiquement
5. ✅ **API REST:** Accès programmatique aux données
6. ✅ **Sécurité:** Authentification + Permissions
7. ✅ **Tests:** 87 tests automatisés (97% couverture)
8. ✅ **Docker:** Application complètement containerisée

---

## 🎓 Questions Fréquentes

### Q: Peut-on modifier le matricule?
**R:** Non, il est généré une seule fois et ne peut pas être changé. C'est intentionnel pour l'unicité.

### Q: Un étudiant peut avoir plusieurs notes dans la même matière?
**R:** Oui, mais à des **dates différentes**. Cela permet d'enregistrer les tests, contrôles et examens.

### Q: Comment la moyenne se calcule?
**R:** Formule pondérée: `Σ(Note × Coefficient) / Σ(Coefficients)`

### Q: Quel est le coefficient par défaut?
**R:** Chaque matière doit avoir un coefficient spécifié. Pas de valeur par défaut.

### Q: Peut-on supprimer un étudiant?
**R:** Oui, et tous ses grades seront supprimés (suppression en cascade).

### Q: L'application est-elle en production?
**R:** Non, c'est une application de **démonstration/développement**. Pour la production, il faudrait:
- Configurer HTTPS
- Utiliser une vraie base de données externe
- Mettre en place un reverse proxy (nginx)
- Configurer le monitoring

---

## 📞 Support Technique

Si quelque chose ne fonctionne pas:

```bash
# Vérifier les logs
docker compose logs -f web

# Redémarrer l'application
docker compose down
docker compose up -d

# Réinitialiser la base de données
docker compose down -v
docker compose up -d
```

---

**Bonne présentation!** 🎉
