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
        
class AlumnoBusquedaTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        # El setUp del padre ya creó self.alumno (Juan Pérez, karate)
        # Creamos alumnos adicionales para testear filtros
        from apps.alumnos.models import Alumno
        import datetime
        self.alumno_mma = Alumno.objects.create(
            nombre='Ana García',
            edad=22,
            telefono='111222333',
            disciplina='mma',
            cinturon='principiante',
            fecha_ingreso=datetime.date.today(),
        )
        self.alumno_verde = Alumno.objects.create(
            nombre='Luis Torres',
            edad=30,
            telefono='444555666',
            disciplina='karate',
            cinturon='verde',
            fecha_ingreso=datetime.date.today(),
        )

    def test_busqueda_por_nombre_parcial(self):
        """Buscar 'juan' debe encontrar 'Juan Pérez'."""
        self.login()
        response = self.client.get(reverse('alumnos:lista') + '?q=juan')
        alumnos = response.context['alumnos']
        self.assertEqual(alumnos.count(), 1)
        self.assertEqual(alumnos.first().nombre, 'Juan Pérez')

    def test_busqueda_insensible_a_mayusculas(self):
        """Buscar 'JUAN' debe encontrar 'Juan Pérez'."""
        self.login()
        response = self.client.get(reverse('alumnos:lista') + '?q=JUAN')
        self.assertEqual(response.context['alumnos'].count(), 1)

    def test_filtro_por_disciplina(self):
        """Filtrar por MMA debe devolver solo alumnos de MMA."""
        self.login()
        response = self.client.get(reverse('alumnos:lista') + '?disciplina=mma')
        alumnos = response.context['alumnos']
        self.assertEqual(alumnos.count(), 1)
        self.assertEqual(alumnos.first().nombre, 'Ana García')

    def test_filtro_por_cinturon(self):
        """Filtrar por verde debe devolver solo alumnos con cinturón verde."""
        self.login()
        response = self.client.get(reverse('alumnos:lista') + '?cinturon=verde')
        alumnos = response.context['alumnos']
        self.assertEqual(alumnos.count(), 1)
        self.assertEqual(alumnos.first().nombre, 'Luis Torres')

    def test_filtros_combinados(self):
        """Combinar disciplina y cinturón debe funcionar correctamente."""
        self.login()
        response = self.client.get(
            reverse('alumnos:lista') + '?disciplina=karate&cinturon=blanco'
        )
        alumnos = response.context['alumnos']
        self.assertEqual(alumnos.count(), 1)
        self.assertEqual(alumnos.first().nombre, 'Juan Pérez')

    def test_sin_resultados_muestra_mensaje(self):
        """Una búsqueda sin resultados debe mostrar el estado vacío."""
        self.login()
        response = self.client.get(reverse('alumnos:lista') + '?q=xyzxyzxyz')
        self.assertEqual(response.context['alumnos'].count(), 0)
        self.assertTrue(response.context['hay_filtros'])

    def test_limpiar_filtros_devuelve_todos(self):
        """Sin parámetros en la URL deben aparecer todos los alumnos activos."""
        self.login()
        response = self.client.get(reverse('alumnos:lista'))
        self.assertEqual(response.context['alumnos'].count(), 3)
        self.assertFalse(response.context['hay_filtros'])