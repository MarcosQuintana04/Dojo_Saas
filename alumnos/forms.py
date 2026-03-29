# alumnos/forms.py

from django import forms
from .models import Alumno, Asistencia, Pago
import datetime

"""
    ModelForm es la herramienta más poderosa de Django para formularios.
    En vez de definir cada campo a mano, Django lee el modelo y genera
    el formulario automáticamente. Solo indicás qué campos incluir.
"""

class AlumnoForm(forms.ModelForm):

    class Meta:
        model = Alumno
        # Listamos los campos que el usuario puede completar.
        # Nota: fecha_ingreso y activo NO están — los manejamos nosotros.
        fields = ['nombre', 'edad', 'telefono', 'email',
                  'disciplina', 'cinturon', 'fecha_ingreso']

        # Personalizamos los widgets (el HTML que se genera para cada campo)
        # para que sean compatibles con Bootstrap
        widgets = {
            'nombre':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'edad':       forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+51 999 999 999'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'opcional'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'cinturon':   forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(
                attrs={'class': 'form-control', 'type':'date'},
                format='%Y-%m-%d'
            ),
        }

        # Etiquetas personalizadas (lo que aparece sobre cada campo)
        labels = {
            'nombre':    'Nombre completo',
            'edad':      'Edad',
            'telefono':  'Teléfono',
            'email':     'Correo electrónico',
            'disciplina':'Disciplina',
            'cinturon':  'Cinturón / Nivel',
            'fecha_ingreso': 'Fecha de ingreso',
        }
        
class AsistenciaForm(forms.ModelForm):

    class Meta:
        model = Asistencia
        fields = ['alumno', 'fecha', 'presente', 'observacion']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            # DateInput con type="date" genera el selector de fecha del navegador
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Opcional...'
            }),
        }
        labels = {
            'alumno': 'Alumno',
            'fecha': 'Fecha',
            'presente': '¿Presente?',
            'observacion': 'Observación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar alumnos activos en el selector
        self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
        # Pre-seleccionar la fecha de hoy
        self.fields['fecha'].initial = datetime.date.today()


class PagoForm(forms.ModelForm):

    class Meta:
        model = Pago
        fields = ['alumno', 'monto', 'fecha_pago', 'mes', 'anio']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'  # permite decimales
            }),
            'fecha_pago': forms.DateInput(  # ← agregar este widget
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'mes': forms.Select(attrs={'class': 'form-select'}),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2025'
            }),
        }
        labels = {
            'alumno': 'Alumno',
            'monto': 'Monto (S/)',
            'fecha_pago':'Fecha de pago',
            'mes': 'Mes',
            'anio': 'Año',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
        hoy = datetime.date.today()
        self.fields['mes'].initial = hoy.month
        self.fields['anio'].initial = hoy.year
        self.fields['fecha_pago'].initial = hoy