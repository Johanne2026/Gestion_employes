# Guide des Tests - Application Employé

## Structure des Tests

Les tests sont organisés dans `employe/tests.py` et couvrent tous les aspects de l'application :

### 1. Tests du Modèle (`EmployeModelTest`)
- Création d'employés
- Représentation string
- Validation des types de champs

### 2. Tests du Formulaire (`EmployeFormTest`)
- Validation avec données valides
- Validation avec email invalide
- Champs requis manquants
- Sauvegarde du formulaire

### 3. Tests du Serializer (`EmployeSerializerTest`)
- Validation des données
- Vérification des champs
- Gestion des erreurs de validation

### 4. Tests de l'API REST (`EmployeAPITest`)
- Liste des employés (GET)
- Ajout d'employé (POST)
- Modification complète (PUT)
- Modification partielle (PATCH)
- Suppression (DELETE)
- Gestion des erreurs 404

### 5. Tests des Vues Django (`EmployeViewTest`)
- Vue index
- Templates utilisés

## Exécution des Tests

### Tous les tests
```bash
python manage.py test
```

### Tests d'une application spécifique
```bash
python manage.py test employe
```

### Tests d'une classe spécifique
```bash
python manage.py test employe.tests.EmployeModelTest
```

### Test spécifique
```bash
python manage.py test employe.tests.EmployeModelTest.test_employe_creation
```

### Avec verbosité
```bash
python manage.py test --verbosity=2
```

### Avec couverture de code
```bash
pip install coverage
coverage run --source='.' manage.py test employe
coverage report
coverage html
```

## Résultats Attendus

Tous les tests devraient passer avec succès :
- 4 tests pour le modèle
- 4 tests pour le formulaire
- 3 tests pour le serializer
- 8 tests pour l'API REST
- 2 tests pour les vues

Total : 21 tests
