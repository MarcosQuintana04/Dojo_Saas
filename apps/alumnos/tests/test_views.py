from django.urls import reverse
from apps.utils_tests import BaseTestCase
from apps.alumnos.models import Alumno
import datetime


class AlumnoViewsAuthTest(BaseTestCase):
    """
    Tests que verifican que las vistas están protegidas por login.
    Un usuario no autenticado debe ser redirigido al login.
    """

    def test_lista_redirige_sin_login(self):
        """Sin login, /alumnos/ debe redirigir a /login/"""
        response = self.client.get(reverse('alumnos:lista'))
        # 302 = redirección
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_lista_accesible_con_login(self):
        """Con login, /alumnos/ debe devolver 200"""
        self.login()
        response = self.client.get(reverse('alumnos:lista'))
        self.assertEqual(response.status_code, 200)

    def test_detalle_redirige_sin_login(self):
        response = self.client.get(reverse('alumnos:detalle', args=[self.alumno.pk]))
        self.assertEqual(response.status_code, 302)

    def test_crear_redirige_sin_login(self):
        response = self.client.get(reverse('alumnos:crear'))
        self.assertEqual(response.status_code, 302)


class AlumnoViewsCRUDTest(BaseTestCase):
    """
    Tests que verifican la lógica de crear, editar y eliminar alumnos.
    """

    def test_lista_muestra_alumnos_activos(self):
        """La lista debe mostrar solo alumnos activos."""
        self.login()
        # Creamos un alumno inactivo
        Alumno.objects.create(
            nombre='Alumno Inactivo', edad=30, telefono='000000000',
            disciplina='karate', cinturon='negro',
            fecha_ingreso=datetime.date.today(),
            activo=False
        )
        response = self.client.get(reverse('alumnos:lista'))
        alumnos = response.context['alumnos']
        # Solo debe aparecer el alumno activo del setUp
        self.assertEqual(alumnos.count(), 1)
        self.assertFalse(any(a.nombre == 'Alumno Inactivo' for a in alumnos))

    def test_crear_alumno_post_valido(self):
        """Un POST válido debe crear el alumno y redirigir a la lista."""
        self.login()
        datos = {
            'nombre': 'Nuevo Alumno',
            'edad': 22,
            'telefono': '123456789',
            'disciplina': 'mma',
            'cinturon': 'principiante',
            'fecha_ingreso': datetime.date.today(),
        }
        response = self.client.post(reverse('alumnos:crear'), datos)
        # Debe redirigir tras crear
        self.assertEqual(response.status_code, 302)
        # El alumno debe existir en la BD
        self.assertTrue(Alumno.objects.filter(nombre='Nuevo Alumno').exists())

    def test_crear_alumno_post_invalido(self):
        """Un POST sin nombre no debe crear el alumno."""
        self.login()
        datos = {'edad': 22}  # faltan campos obligatorios
        response = self.client.post(reverse('alumnos:crear'), datos)
        # Debe volver al formulario (200), no redirigir
        self.assertEqual(response.status_code, 200)

    def test_eliminar_alumno_hace_soft_delete(self):
        """Eliminar un alumno debe marcarlo como inactivo, no borrarlo."""
        self.login()
        self.client.post(reverse('alumnos:eliminar', args=[self.alumno.pk]))
        self.alumno.refresh_from_db()  # recargar desde la BD
        self.assertFalse(self.alumno.activo)