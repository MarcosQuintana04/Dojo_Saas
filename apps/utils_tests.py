from django.test import TestCase, Client
from django.contrib.auth.models import User
import datetime
from apps.alumnos.models import Alumno


class BaseTestCase(TestCase):
    """
    Clase base con setup común para todos los tests del proyecto.
    Cada test que herede de esta clase tendrá disponible:
    - self.client: cliente HTTP para simular peticiones
    - self.user: usuario autenticado
    - self.alumno: alumno de prueba
    """

    def setUp(self):
        """
        setUp se ejecuta ANTES de cada test individual.
        Acá preparamos el estado inicial que necesita cada test.
        """
        # Cliente HTTP — simula un navegador
        self.client = Client()

        # Usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Alumno de prueba
        self.alumno = Alumno.objects.create(
            nombre='Juan Pérez',
            edad=25,
            telefono='999888777',
            disciplina='karate',
            cinturon='blanco',
            fecha_ingreso=datetime.date.today(),
            activo=True
        )

    def login(self):
        """Helper para no repetir el login en cada test."""
        self.client.login(username='testuser', password='testpass123')