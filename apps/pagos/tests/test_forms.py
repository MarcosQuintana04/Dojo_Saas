from apps.utils_tests import BaseTestCase
from apps.pagos.forms import PagoForm
import datetime


class PagoFormTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.hoy = datetime.date.today()

    def datos_validos(self):
        return {
            'alumno': self.alumno.pk,
            'monto': '70.00',
            'fecha_pago': self.hoy,
            'mes': self.hoy.month,
            'anio': self.hoy.year,
        }

    def test_form_valido_con_datos_correctos(self):
        form = PagoForm(data=self.datos_validos())
        self.assertTrue(form.is_valid())

    def test_form_invalido_sin_alumno(self):
        datos = self.datos_validos()
        del datos['alumno']
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('alumno', form.errors)

    def test_form_invalido_sin_monto(self):
        datos = self.datos_validos()
        del datos['monto']
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)

    def test_form_invalido_monto_negativo(self):
        """El monto no debería ser negativo."""
        datos = self.datos_validos()
        datos['monto'] = '-50.00'
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())

    def test_form_invalido_sin_mes(self):
        datos = self.datos_validos()
        del datos['mes']
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('mes', form.errors)

    def test_form_invalido_sin_anio(self):
        datos = self.datos_validos()
        del datos['anio']
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('anio', form.errors)

    def test_form_invalido_mes_fuera_de_rango(self):
        """El mes debe estar entre 1 y 12."""
        datos = self.datos_validos()
        datos['mes'] = 13
        form = PagoForm(data=datos)
        self.assertFalse(form.is_valid())

    def test_solo_muestra_alumnos_activos(self):
        """El selector de alumnos solo debe mostrar alumnos activos."""
        from apps.alumnos.models import Alumno
        Alumno.objects.create(
            nombre='Inactivo Test',
            edad=30,
            telefono='000000000',
            disciplina='karate',
            cinturon='negro',
            fecha_ingreso=datetime.date.today(),
            activo=False
        )
        form = PagoForm()
        alumnos_en_form = list(form.fields['alumno'].queryset)
        nombres = [a.nombre for a in alumnos_en_form]
        self.assertNotIn('Inactivo Test', nombres)

    def test_pre_selecciona_mes_actual(self):
        """El formulario debe pre-seleccionar el mes actual."""
        form = PagoForm()
        self.assertEqual(form.fields['mes'].initial, self.hoy.month)

    def test_pre_selecciona_anio_actual(self):
        """El formulario debe pre-seleccionar el año actual."""
        form = PagoForm()
        self.assertEqual(form.fields['anio'].initial, self.hoy.year)