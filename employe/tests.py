from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Employe
from .forms import EmployeForm
from .serializers import EmployeSerializer


class EmployeModelTest(TestCase):
    """Tests pour le modèle Employe"""
    
    def setUp(self):
        self.employe = Employe.objects.create(
            nom="Jean Dupont",
            email="jean.dupont@example.com",
            poste="Développeur",
            salaire=Decimal("50000.00")
        )
    
    def test_employe_creation(self):
        """Test la création d'un employé"""
        self.assertEqual(self.employe.nom, "Jean Dupont")
        self.assertEqual(self.employe.email, "jean.dupont@example.com")
        self.assertEqual(self.employe.poste, "Développeur")
        self.assertEqual(self.employe.salaire, Decimal("50000.00"))
    
    def test_employe_str(self):
        """Test la représentation string d'un employé"""
        self.assertEqual(str(self.employe), "Jean Dupont")
    
    def test_employe_fields(self):
        """Test les types de champs du modèle"""
        self.assertIsInstance(self.employe.nom, str)
        self.assertIsInstance(self.employe.email, str)
        self.assertIsInstance(self.employe.poste, str)
        self.assertIsInstance(self.employe.salaire, Decimal)


class EmployeFormTest(TestCase):
    """Tests pour le formulaire EmployeForm"""
    
    def test_form_valid_data(self):
        """Test le formulaire avec des données valides"""
        form_data = {
            'nom': 'Marie Martin',
            'email': 'marie.martin@example.com',
            'poste': 'Designer',
            'salaire': '45000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_email(self):
        """Test le formulaire avec un email invalide"""
        form_data = {
            'nom': 'Marie Martin',
            'email': 'email_invalide',
            'poste': 'Designer',
            'salaire': '45000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_missing_required_fields(self):
        """Test le formulaire avec des champs manquants"""
        form_data = {
            'nom': 'Marie Martin'
        }
        form = EmployeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
    
    def test_form_save(self):
        """Test la sauvegarde du formulaire"""
        form_data = {
            'nom': 'Pierre Durand',
            'email': 'pierre.durand@example.com',
            'poste': 'Manager',
            'salaire': '60000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertTrue(form.is_valid())
        employe = form.save()
        self.assertEqual(employe.nom, 'Pierre Durand')
        self.assertEqual(Employe.objects.count(), 1)


class EmployeSerializerTest(TestCase):
    """Tests pour le serializer EmployeSerializer"""
    
    def setUp(self):
        self.employe_data = {
            'nom': 'Sophie Bernard',
            'email': 'sophie.bernard@example.com',
            'poste': 'Analyste',
            'salaire': '48000.00'
        }
        self.employe = Employe.objects.create(**self.employe_data)
    
    def test_serializer_with_valid_data(self):
        """Test le serializer avec des données valides"""
        serializer = EmployeSerializer(data=self.employe_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_contains_expected_fields(self):
        """Test que le serializer contient tous les champs attendus"""
        serializer = EmployeSerializer(instance=self.employe)
        data = serializer.data
        expected_fields = {'id', 'nom', 'email', 'poste', 'salaire'}
        self.assertEqual(set(data.keys()), expected_fields)
    
    def test_serializer_invalid_email(self):
        """Test le serializer avec un email invalide"""
        invalid_data = self.employe_data.copy()
        invalid_data['email'] = 'email_invalide'
        serializer = EmployeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


class EmployeAPITest(APITestCase):
    """Tests pour les vues API REST"""
    
    def setUp(self):
        self.employe1 = Employe.objects.create(
            nom="Alice Dubois",
            email="alice.dubois@example.com",
            poste="Chef de projet",
            salaire=Decimal("55000.00")
        )
        self.employe2 = Employe.objects.create(
            nom="Bob Leroy",
            email="bob.leroy@example.com",
            poste="Développeur",
            salaire=Decimal("52000.00")
        )
    
    def test_liste_employes(self):
        """Test la récupération de la liste des employés"""
        response = self.client.get('/employe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_ajouter_employe(self):
        """Test l'ajout d'un nouvel employé"""
        data = {
            'nom': 'Claire Petit',
            'email': 'claire.petit@example.com',
            'poste': 'RH',
            'salaire': '47000.00'
        }
        response = self.client.post('/employe/ajouter/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employe.objects.count(), 3)
        self.assertEqual(Employe.objects.last().nom, 'Claire Petit')
    
    def test_ajouter_employe_donnees_invalides(self):
        """Test l'ajout d'un employé avec des données invalides"""
        data = {
            'nom': 'Test',
            'email': 'email_invalide',
            'poste': 'Test'
        }
        response = self.client.post('/employe/ajouter/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_modifier_employe(self):
        """Test la modification d'un employé"""
        data = {
            'nom': 'Alice Dubois Modifié',
            'email': 'alice.nouveau@example.com',
            'poste': 'Directrice',
            'salaire': '65000.00'
        }
        response = self.client.put(
            f'/employe/modifier/{self.employe1.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employe1.refresh_from_db()
        self.assertEqual(self.employe1.nom, 'Alice Dubois Modifié')
        self.assertEqual(self.employe1.salaire, Decimal('65000.00'))
    
    def test_modifier_employe_partiel(self):
        """Test la modification partielle d'un employé"""
        data = {'salaire': '60000.00'}
        response = self.client.patch(
            f'/employe/modifier/{self.employe1.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employe1.refresh_from_db()
        self.assertEqual(self.employe1.salaire, Decimal('60000.00'))
    
    def test_supprimer_employe(self):
        """Test la suppression d'un employé"""
        response = self.client.delete(f'/employe/supprimer/{self.employe1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employe.objects.count(), 1)
        self.assertFalse(Employe.objects.filter(id=self.employe1.id).exists())
    
    def test_recuperer_employe_inexistant(self):
        """Test la récupération d'un employé qui n'existe pas"""
        response = self.client.get('/employe/modifier/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_supprimer_employe_inexistant(self):
        """Test la suppression d'un employé qui n'existe pas"""
        response = self.client.delete('/employe/supprimer/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeViewTest(TestCase):
    """Tests pour les vues Django"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test la vue index"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employe/index.html')
    
    def test_index_view_uses_correct_template(self):
        """Test que la vue index utilise le bon template"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'employe/index.html')

