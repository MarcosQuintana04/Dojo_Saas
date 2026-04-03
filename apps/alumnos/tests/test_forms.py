from django.test import TestCase
from apps.alumnos.forms import AlumnoForm
import datetime


class AlumnoFormTest(TestCase):

    def datos_validos(self):
        """Datos base válidos — los tests los modifican según necesiten."""
        return {
            'nombre': 'Test Alumno',
            'edad': 25,
            'telefono': '999888777',
            'disciplina': 'karate',
            'cinturon': 'blanco',
            'fecha_ingreso': datetime.date.today(),
        }

    def test_form_valido_con_datos_correctos(self):
        form = AlumnoForm(data=self.datos_validos())
        self.assertTrue(form.is_valid())

    def test_form_invalido_sin_nombre(self):
        datos = self.datos_validos()
        del datos['nombre']
        form = AlumnoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_form_invalido_sin_disciplina(self):
        datos = self.datos_validos()
        del datos['disciplina']
        form = AlumnoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('disciplina', form.errors)

    def test_email_opcional(self):
        """El email es opcional — el form debe ser válido sin él."""
        datos = self.datos_validos()
        # email no está en datos_validos, así que ya es opcional
        form = AlumnoForm(data=datos)
        self.assertTrue(form.is_valid())

    def test_email_invalido_falla_validacion(self):
        datos = self.datos_validos()
        datos['email'] = 'esto-no-es-un-email'
        form = AlumnoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)