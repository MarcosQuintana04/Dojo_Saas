from django.urls import reverse
from apps.utils_tests import BaseTestCase
from apps.pagos.models import Pago
from apps.alumnos.models import Alumno
import datetime


class DeudoresLogicaTest(BaseTestCase):

    def setUp(self):
        super().setUp()  # importante: llamar al setUp del padre
        self.hoy = datetime.date.today()

    def test_alumno_sin_pago_aparece_como_deudor(self):
        """Un alumno activo sin pago este mes debe aparecer en deudores."""
        self.login()
        response = self.client.get(reverse('pagos:deudores'))
        deudores = response.context['deudores']
        self.assertIn(self.alumno, deudores)

    def test_alumno_con_pago_no_aparece_como_deudor(self):
        """Un alumno que pagó este mes NO debe aparecer en deudores."""
        # Registramos el pago
        Pago.objects.create(
            alumno=self.alumno,
            monto=70,
            fecha_pago=self.hoy,
            mes=self.hoy.month,
            anio=self.hoy.year
        )
        self.login()
        response = self.client.get(reverse('pagos:deudores'))
        deudores = response.context['deudores']
        self.assertNotIn(self.alumno, deudores)

    def test_pago_mes_anterior_no_exime_de_deuda_actual(self):
        """
        Pagar el mes anterior NO significa que está al día este mes.
        Este test verifica la regla de negocio más importante del sistema.
        """
        mes_anterior = self.hoy.month - 1 if self.hoy.month > 1 else 12
        anio = self.hoy.year if self.hoy.month > 1 else self.hoy.year - 1

        Pago.objects.create(
            alumno=self.alumno,
            monto=70,
            fecha_pago=self.hoy,
            mes=mes_anterior,
            anio=anio
        )
        self.login()
        response = self.client.get(reverse('pagos:deudores'))
        deudores = response.context['deudores']
        # Sigue siendo deudor del mes actual
        self.assertIn(self.alumno, deudores)

    def test_alumno_inactivo_no_aparece_en_deudores(self):
        """Los alumnos dados de baja no deben aparecer en deudores."""
        self.alumno.activo = False
        self.alumno.save()
        self.login()
        response = self.client.get(reverse('pagos:deudores'))
        deudores = response.context['deudores']
        self.assertNotIn(self.alumno, deudores)