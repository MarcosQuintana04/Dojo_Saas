from django.db import models
from django.contrib.auth.models import User
from apps.alumnos.models import Alumno


class PerfilAlumno(models.Model):
    """
    Puente entre el sistema de autenticación de Django
    y el modelo Alumno del dojo.
    OneToOneField garantiza que cada usuario tiene exactamente
    un alumno y cada alumno tiene exactamente un usuario.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_alumno'
    )
    alumno = models.OneToOneField(
        Alumno,
        on_delete=models.CASCADE,
        related_name='perfil_usuario'
    )

    def __str__(self):
        return f'{self.user.username} → {self.alumno.nombre}'

    class Meta:
        verbose_name = 'Perfil de Alumno'
        verbose_name_plural = 'Perfiles de Alumnos'
