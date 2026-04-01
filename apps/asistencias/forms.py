import datetime
from django import forms
from .models import Asistencia
from apps.alumnos.models import Alumno

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['alumno', 'fecha', 'presente', 'observacion']
        widgets = {
            'alumno':      forms.Select(attrs={'class': 'form-select'}),
            'fecha':       forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'presente':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
        self.fields['fecha'].initial = datetime.date.today()