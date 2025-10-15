from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer


class TicketModelTest(TestCase):
    """Tests para el modelo Ticket"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_ticket(self):
        """Test crear un ticket con todos los campos requeridos"""
        ticket = Ticket.objects.create(
            titulo='Test Ticket',
            descripcion='Esta es una descripción de prueba',
            estado='abierto',
            prioridad='media',
            usuario=self.user
        )
        self.assertEqual(ticket.titulo, 'Test Ticket')
        self.assertEqual(ticket.descripcion, 'Esta es una descripción de prueba')
        self.assertEqual(ticket.estado, 'abierto')
        self.assertEqual(ticket.prioridad, 'media')
        self.assertEqual(ticket.usuario, self.user)
    
    def test_ticket_str_method(self):
        """Test el método __str__ del modelo Ticket"""
        ticket = Ticket.objects.create(
            titulo='Ticket de Prueba',
            descripcion='Descripción',
            usuario=self.user
        )
        expected_str = f"{ticket.titulo} - Abierto"
        self.assertEqual(str(ticket), expected_str)
    
    def test_ticket_default_values(self):
        """Test valores por defecto del ticket"""
        ticket = Ticket.objects.create(
            titulo='Ticket con Defaults',
            descripcion='Descripción',
            usuario=self.user
        )
        self.assertEqual(ticket.estado, 'abierto')
        self.assertEqual(ticket.prioridad, 'media')
    
    def test_ticket_ordering(self):
        """Test ordenamiento de tickets por fecha de creación"""
        ticket1 = Ticket.objects.create(
            titulo='Primer Ticket',
            descripcion='Descripción 1',
            usuario=self.user
        )
        ticket2 = Ticket.objects.create(
            titulo='Segundo Ticket',
            descripcion='Descripción 2',
            usuario=self.user
        )
        tickets = Ticket.objects.all()
        self.assertEqual(tickets[0], ticket2)  # El más reciente primero
        self.assertEqual(tickets[1], ticket1)


class TicketAPITest(APITestCase):
    """Tests para la API de Tickets"""
    
    def setUp(self):
        """Configuración inicial para las pruebas de API"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_ticket_via_api(self):
        """Test crear un ticket a través de la API"""
        data = {
            'titulo': 'API Test Ticket',
            'descripcion': 'Creado mediante API',
            'estado': 'abierto',
            'prioridad': 'alta',
            'usuario': self.user.id
        }
        response = self.client.post('/api/tickets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().titulo, 'API Test Ticket')
    
    def test_list_tickets_via_api(self):
        """Test listar tickets a través de la API"""
        Ticket.objects.create(
            titulo='Ticket 1',
            descripcion='Descripción 1',
            usuario=self.user
        )
        Ticket.objects.create(
            titulo='Ticket 2',
            descripcion='Descripción 2',
            usuario=self.user
        )
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Con paginación, la respuesta incluye 'results'
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_ticket_via_api(self):
        """Test obtener un ticket específico a través de la API"""
        ticket = Ticket.objects.create(
            titulo='Ticket Específico',
            descripcion='Descripción específica',
            usuario=self.user
        )
        response = self.client.get(f'/api/tickets/{ticket.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Ticket Específico')
    
    def test_update_ticket_via_api(self):
        """Test actualizar un ticket a través de la API"""
        ticket = Ticket.objects.create(
            titulo='Ticket Original',
            descripcion='Descripción original',
            usuario=self.user
        )
        data = {
            'titulo': 'Ticket Actualizado',
            'descripcion': 'Descripción actualizada',
            'estado': 'en_progreso',
            'prioridad': 'alta',
            'usuario': self.user.id
        }
        response = self.client.put(f'/api/tickets/{ticket.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.titulo, 'Ticket Actualizado')
        self.assertEqual(ticket.estado, 'en_progreso')
    
    def test_delete_ticket_via_api(self):
        """Test eliminar un ticket a través de la API"""
        ticket = Ticket.objects.create(
            titulo='Ticket a Eliminar',
            descripcion='Este ticket será eliminado',
            usuario=self.user
        )
        response = self.client.delete(f'/api/tickets/{ticket.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 0)
    
    def test_filter_tickets_by_estado(self):
        """Test filtrar tickets por estado"""
        Ticket.objects.create(
            titulo='Ticket Abierto',
            descripcion='Estado: abierto',
            estado='abierto',
            usuario=self.user
        )
        Ticket.objects.create(
            titulo='Ticket Cerrado',
            descripcion='Estado: cerrado',
            estado='cerrado',
            usuario=self.user
        )
        response = self.client.get('/api/tickets/?estado=abierto')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Con paginación, la respuesta incluye 'results'
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['estado'], 'abierto')
    
    def test_authentication_required(self):
        """Test que la autenticación es requerida"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
