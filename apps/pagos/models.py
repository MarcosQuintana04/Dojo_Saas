from django.db import models
from apps.alumnos.models import Alumno

class Pago(models.Model):
    MES_CHOICES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'),
        (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
        (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'),
        (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'),
    ]
    alumno     = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='pagos')
    monto      = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pago = models.DateField()
    mes        = models.PositiveIntegerField(choices=MES_CHOICES)
    anio       = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.alumno.nombre} — {self.get_mes_display()} {self.anio}"

    class Meta:
        ordering = ['-anio', '-mes']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        unique_together = ['alumno', 'mes', 'anio']
