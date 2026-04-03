from django.urls import reverse
from apps.utils_tests import BaseTestCase
from apps.asistencias.models import Asistencia
import datetime


class AsistenciaAuthTest(BaseTestCase):

    def test_hoy_redirige_sin_login(self):
        response = self.client.get(reverse('asistencias:hoy'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_hoy_accesible_con_login(self):
        self.login()
        response = self.client.get(reverse('asistencias:hoy'))
        self.assertEqual(response.status_code, 200)


class AsistenciaLogicaTest(BaseTestCase):

    def test_registrar_asistencia_presente(self):
        """Un POST válido debe crear la asistencia como presente."""
        self.login()
        datos = {
            'alumno': self.alumno.pk,
            'fecha': datetime.date.today(),
            'presente': True,
        }
        self.client.post(reverse('asistencias:registrar'), datos)
        self.assertTrue(
            Asistencia.objects.filter(
                alumno=self.alumno,
                fecha=datetime.date.today(),
                presente=True
            ).exists()
        )

    def test_registrar_asistencia_ausente(self):
        """Un POST con presente=False debe registrar al alumno como ausente."""
        self.login()
        datos = {
            'alumno': self.alumno.pk,
            'fecha': datetime.date.today(),
            # presente no incluido = False
        }
        self.client.post(reverse('asistencias:registrar'), datos)
        self.assertTrue(
            Asistencia.objects.filter(
                alumno=self.alumno,
                fecha=datetime.date.today(),
                presente=False
            ).exists()
        )

    def test_vista_hoy_muestra_solo_asistencias_de_hoy(self):
        """La vista de hoy solo debe mostrar asistencias del día actual."""
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)

        Asistencia.objects.create(alumno=self.alumno, fecha=hoy, presente=True)
        Asistencia.objects.create(
            alumno=self.alumno,
            fecha=ayer,
            presente=True
        )

        self.login()
        response = self.client.get(reverse('asistencias:hoy'))
        asistencias = response.context['asistencias']
        self.assertEqual(asistencias.count(), 1)
        self.assertEqual(asistencias.first().fecha, hoy)

    def test_porcentaje_asistencia_en_historial(self):
        """El historial debe calcular correctamente el porcentaje."""
        hoy = datetime.date.today()
        Asistencia.objects.create(alumno=self.alumno, fecha=hoy, presente=True)
        Asistencia.objects.create(
            alumno=self.alumno,
            fecha=hoy - datetime.timedelta(days=1),
            presente=False
        )

        self.login()
        response = self.client.get(
            reverse('asistencias:historial', args=[self.alumno.pk])
        )
        # 1 de 2 = 50%
        self.assertEqual(response.context['porcentaje'], 50.0)