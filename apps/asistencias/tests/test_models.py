from apps.utils_tests import BaseTestCase
from apps.asistencias.models import Asistencia
import datetime


class AsistenciaModelTest(BaseTestCase):

    def test_str_muestra_estado_y_alumno(self):
        """El __str__ debe mostrar el estado y el nombre del alumno."""
        asistencia = Asistencia.objects.create(
            alumno=self.alumno,
            fecha=datetime.date.today(),
            presente=True
        )
        self.assertIn('✓', str(asistencia))
        self.assertIn(self.alumno.nombre, str(asistencia))

    def test_str_ausente_muestra_cruz(self):
        asistencia = Asistencia.objects.create(
            alumno=self.alumno,
            fecha=datetime.date.today(),
            presente=False
        )
        self.assertIn('✗', str(asistencia))

    def test_no_duplicar_asistencia_mismo_dia(self):
        """
        No se puede registrar dos asistencias del mismo alumno
        en el mismo día — lo garantiza unique_together.
        """
        from django.db import IntegrityError
        Asistencia.objects.create(
            alumno=self.alumno,
            fecha=datetime.date.today(),
            presente=True
        )
        with self.assertRaises(IntegrityError):
            Asistencia.objects.create(
                alumno=self.alumno,
                fecha=datetime.date.today(),
                presente=False
            )

    def test_ordenamiento_por_fecha_descendente(self):
        """Las asistencias deben venir ordenadas de más reciente a más antigua."""
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)

        Asistencia.objects.create(alumno=self.alumno, fecha=ayer, presente=True)
        Asistencia.objects.create(alumno=self.alumno, fecha=hoy, presente=True)

        asistencias = list(Asistencia.objects.all())
        self.assertEqual(asistencias[0].fecha, hoy)
        self.assertEqual(asistencias[1].fecha, ayer)