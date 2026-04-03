import datetime
from django import forms
from .models import Pago
from apps.alumnos.models import Alumno

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['alumno', 'monto', 'fecha_pago', 'mes', 'anio']
        widgets = {
            'alumno':     forms.Select(attrs={'class': 'form-select'}),
            'monto':      forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha_pago': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'mes':        forms.Select(attrs={'class': 'form-select'}),
            'anio':       forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'alumno':     'Alumno',
            'monto':      'Monto (S/)',
            'fecha_pago': 'Fecha de pago',
            'mes':        'Mes',
            'anio':       'Año',
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None and monto < 0:
            raise forms.ValidationError('El monto debe ser mayor o igual a cero.')
        return monto
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].queryset = Alumno.objects.filter(activo=True)
        hoy = datetime.date.today()
        self.fields['mes'].initial = hoy.month
        self.fields['anio'].initial = hoy.year
        self.fields['fecha_pago'].initial = hoy