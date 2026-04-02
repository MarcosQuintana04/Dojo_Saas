from django import forms
from .models import Clase, Inscripcion
from apps.alumnos.models import Alumno


class ClaseForm(forms.ModelForm):

    class Meta:
        model = Clase
        fields = ['nombre', 'disciplina', 'dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'nombre':      forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ej: Karate Principiantes'
            }),
            'disciplina':  forms.Select(attrs={'class': 'form-select'}),
            'dia':         forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
            'hora_fin':    forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'}
            ),
        }
        labels = {
            'nombre':      'Nombre de la clase',
            'disciplina':  'Disciplina',
            'dia':         'Día',
            'hora_inicio': 'Hora de inicio',
            'hora_fin':    'Hora de fin',
        }


class InscripcionForm(forms.ModelForm):
    """
    Formulario para inscribir un alumno a una clase.
    El campo 'clase' viene fijo desde la vista — el usuario solo elige el alumno.
    """
    class Meta:
        model = Inscripcion
        fields = ['alumno']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'alumno': 'Alumno',
        }

    def __init__(self, clase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar alumnos activos que NO están ya inscritos en esta clase
        ya_inscritos = clase.alumnos.values_list('id', flat=True)
        self.fields['alumno'].queryset = Alumno.objects.filter(
            activo=True
        ).exclude(id__in=ya_inscritos)