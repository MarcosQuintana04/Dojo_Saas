from django import forms
from .models import ConfiguracionDojo


class ConfiguracionDojoForm(forms.ModelForm):

    class Meta:
        model = ConfiguracionDojo
        fields = ['nombre', 'telefono', 'direccion', 'mensaje_bienvenida']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del dojo'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+51 999 999 999'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección del dojo'
            }),
            'mensaje_bienvenida': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mensaje para nuevos alumnos...'
            }),
        }
        labels = {
            'nombre':             'Nombre del dojo',
            'telefono':           'Teléfono de contacto',
            'direccion':          'Dirección',
            'mensaje_bienvenida': 'Mensaje de bienvenida',
        }