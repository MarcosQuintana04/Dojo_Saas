from django import forms
from django.contrib.auth.models import User
from .models import PerfilAlumno
from apps.alumnos.models import Alumno


class CrearCuentaAlumnoForm(forms.Form):
    """
    Formulario para que el admin cree una cuenta
    para un alumno existente.
    """
    alumno   = forms.ModelChoiceField(
        queryset=Alumno.objects.none(),  # se llena en __init__
        label='Alumno',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ej: juan.perez'
        })
    )
    password = forms.CharField(
        label='Contraseña temporal',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'El alumno puede cambiarla después'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar alumnos activos que NO tienen cuenta todavía
        alumnos_con_cuenta = PerfilAlumno.objects.values_list('alumno_id', flat=True)
        self.fields['alumno'].queryset = Alumno.objects.filter(
            activo=True
        ).exclude(id__in=alumnos_con_cuenta)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Ese nombre de usuario ya existe.')
        return username