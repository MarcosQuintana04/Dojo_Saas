# alumnos/forms.py

from django import forms
from .models import Alumno


class AlumnoForm(forms.ModelForm):
    """
    ModelForm es la herramienta más poderosa de Django para formularios.
    En vez de definir cada campo a mano, Django lee el modelo y genera
    el formulario automáticamente. Solo indicás qué campos incluir.
    """

    class Meta:
        model = Alumno
        # Listamos los campos que el usuario puede completar.
        # Nota: fecha_ingreso y activo NO están — los manejamos nosotros.
        fields = ['nombre', 'edad', 'telefono', 'email',
                  'disciplina', 'cinturon']

        # Personalizamos los widgets (el HTML que se genera para cada campo)
        # para que sean compatibles con Bootstrap
        widgets = {
            'nombre':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'edad':       forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+51 999 999 999'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'opcional'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'cinturon':   forms.Select(attrs={'class': 'form-select'}),
        }

        # Etiquetas personalizadas (lo que aparece sobre cada campo)
        labels = {
            'nombre':    'Nombre completo',
            'edad':      'Edad',
            'telefono':  'Teléfono',
            'email':     'Correo electrónico',
            'disciplina':'Disciplina',
            'cinturon':  'Cinturón / Nivel',
        }