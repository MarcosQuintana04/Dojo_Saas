from django.db import IntegrityError
from apps.utils_tests import BaseTestCase
from apps.pagos.models import Pago
import datetime


class PagoModelTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.hoy = datetime.date.today()

    def test_str_muestra_alumno_mes_anio(self):
        pago = Pago.objects.create(
            alumno=self.alumno,
            monto=70,
            fecha_pago=self.hoy,
            mes=self.hoy.month,
            anio=self.hoy.year
        )
        self.assertIn(self.alumno.nombre, str(pago))

    def test_no_duplicar_pago_mismo_mes(self):
        """
        No se puede registrar dos pagos del mismo alumno
        en el mismo mes y año — lo garantiza unique_together.
        """
        Pago.objects.create(
            alumno=self.alumno,
            monto=70,
            fecha_pago=self.hoy,
            mes=self.hoy.month,
            anio=self.hoy.year
        )
        with self.assertRaises(IntegrityError):
            Pago.objects.create(
                alumno=self.alumno,
                monto=70,
                fecha_pago=self.hoy,
                mes=self.hoy.month,
                anio=self.hoy.year
            )