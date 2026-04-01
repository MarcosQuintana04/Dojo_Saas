from django.db import models
from apps.alumnos.models import Alumno

class Asistencia(models.Model):
    alumno      = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='asistencias')
    fecha       = models.DateField()
    presente    = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        estado = "✓" if self.presente else "✗"
        return f"{estado} {self.alumno.nombre} — {self.fecha}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ['alumno', 'fecha']
