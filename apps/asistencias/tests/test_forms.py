from django.test import TestCase
from apps.asistencias.forms import AsistenciaForm
from apps.utils_tests import BaseTestCase
import datetime


class AsistenciaFormTest(BaseTestCase):

    def datos_validos(self):
        return {
            'alumno': self.alumno.pk,
            'fecha': datetime.date.today(),
            'presente': True,
        }

    def test_form_valido_con_datos_correctos(self):
        form = AsistenciaForm(data=self.datos_validos())
        self.assertTrue(form.is_valid())

    def test_form_invalido_sin_alumno(self):
        datos = self.datos_validos()
        del datos['alumno']
        form = AsistenciaForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('alumno', form.errors)

    def test_form_invalido_sin_fecha(self):
        datos = self.datos_validos()
        del datos['fecha']
        form = AsistenciaForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha', form.errors)

    def test_form_invalido_fecha_incorrecta(self):
        datos = self.datos_validos()
        datos['fecha'] = 'no-es-una-fecha'
        form = AsistenciaForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha', form.errors)

    def test_presente_es_false_por_defecto(self):
        """
        Si no se marca presente, el campo debe ser False.
        Importante verificarlo porque es un checkbox.
        """
        datos = self.datos_validos()
        del datos['presente']
        form = AsistenciaForm(data=datos)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['presente'])

    def test_solo_muestra_alumnos_activos(self):
        """
        El selector de alumnos solo debe mostrar alumnos activos.
        """
        from apps.alumnos.models import Alumno
        # Creamos un alumno inactivo
        Alumno.objects.create(
            nombre='Inactivo Test',
            edad=30,
            telefono='000000000',
            disciplina='karate',
            cinturon='negro',
            fecha_ingreso=datetime.date.today(),
            activo=False
        )
        form = AsistenciaForm()
        alumnos_en_form = list(form.fields['alumno'].queryset)
        nombres = [a.nombre for a in alumnos_en_form]
        self.assertNotIn('Inactivo Test', nombres)