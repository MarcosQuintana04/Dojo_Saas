from apps.utils_tests import BaseTestCase
from apps.alumnos.models import Alumno
import datetime


class AlumnoModelTest(BaseTestCase):

    def test_str_devuelve_nombre_y_disciplina(self):
        """
        El __str__ del alumno debe incluir su nombre y disciplina.
        Este test verifica que lo que definimos en el modelo funciona.
        """
        self.assertIn('Juan Pérez', str(self.alumno))
        self.assertIn('Karate', str(self.alumno))

    def test_alumno_activo_por_defecto(self):
        """
        Al crear un alumno sin especificar 'activo',
        debe quedar como True por defecto.
        """
        alumno = Alumno.objects.create(
            nombre='Ana García',
            edad=20,
            telefono='111222333',
            disciplina='mma',
            cinturon='principiante',
            fecha_ingreso=datetime.date.today(),
        )
        self.assertTrue(alumno.activo)

    def test_soft_delete(self):
        """
        Al dar de baja un alumno, debe quedar activo=False
        pero seguir existiendo en la base de datos.
        """
        self.alumno.activo = False
        self.alumno.save()

        # El alumno sigue existiendo
        self.assertEqual(Alumno.objects.filter(pk=self.alumno.pk).count(), 1)
        # Pero no aparece en activos
        self.assertEqual(Alumno.objects.filter(activo=True, pk=self.alumno.pk).count(), 0)

    def test_ordenamiento_por_nombre(self):
        """
        Los alumnos deben venir ordenados por nombre (definido en Meta).
        """
        Alumno.objects.create(
            nombre='Zoe Torres', edad=22, telefono='444555666',
            disciplina='karate', cinturon='verde',
            fecha_ingreso=datetime.date.today()
        )
        Alumno.objects.create(
            nombre='Ana López', edad=18, telefono='777888999',
            disciplina='mma', cinturon='principiante',
            fecha_ingreso=datetime.date.today()
        )
        alumnos = list(Alumno.objects.filter(activo=True))
        nombres = [a.nombre for a in alumnos]
        self.assertEqual(nombres, sorted(nombres))