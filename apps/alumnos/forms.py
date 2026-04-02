import datetime
from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'edad', 'telefono', 'email',
                  'disciplina', 'cinturon', 'fecha_ingreso', 'foto']
        widgets = {
            'nombre':        forms.TextInput(attrs={'class': 'form-control'}),
            'edad':          forms.NumberInput(attrs={'class': 'form-control'}),
            'telefono':      forms.TextInput(attrs={'class': 'form-control'}),
            'email':         forms.EmailInput(attrs={'class': 'form-control'}),
            'disciplina':    forms.Select(attrs={'class': 'form-select'}),
            'cinturon':      forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre':        'Nombre completo',
            'edad':          'Edad',
            'telefono':      'Teléfono',
            'email':         'Correo electrónico',
            'disciplina':    'Disciplina',
            'cinturon':      'Cinturón / Nivel',
            'fecha_ingreso': 'Fecha de ingreso',
            'foto':          'Foto de perfil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['fecha_ingreso'].initial = datetime.date.today()