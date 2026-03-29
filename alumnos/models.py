from django.db import models

# ─────────────────────────────────────────
# MODELO: Alumno
# ─────────────────────────────────────────
class Alumno(models.Model):

    # Opciones para el campo "disciplina"
    # Esto es una buena práctica: en vez de escribir strings sueltos
    # como "karate" o "mma" por todo el código, los centralizamos aquí.
    # Si mañana querés cambiar "mma" por "MMA", lo cambiás en un solo lugar.
    DISCIPLINA_CHOICES = [
        ('karate', 'Karate'),
        ('mma', 'MMA'),
        ('ambas', 'Ambas'),
    ]

    CINTURON_CHOICES = [
        ('blanco', 'Blanco'),
        ('amarillo', 'Amarillo'),
        ('naranja', 'Naranja'),
        ('verde', 'Verde'),
        ('azul', 'Azul'),
        ('marron', 'Marrón'),
        ('negro', 'Negro'),
        # Para MMA podés usar niveles
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    nombre       = models.CharField(max_length=100)
    edad         = models.PositiveIntegerField()
    telefono     = models.CharField(max_length=20)
    email        = models.EmailField(blank=True, null=True)  # opcional
    disciplina   = models.CharField(max_length=10, choices=DISCIPLINA_CHOICES)
    cinturon     = models.CharField(max_length=20, choices=CINTURON_CHOICES)
    fecha_ingreso = models.DateField(auto_now_add=True)
    activo       = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_disciplina_display()})"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'


# ─────────────────────────────────────────
# MODELO: Asistencia
# ─────────────────────────────────────────
class Asistencia(models.Model):

    # ForeignKey es la relación "muchos a uno"
    # on_delete=CASCADE significa: si se borra el alumno,
    # se borran también todas sus asistencias.
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
        # Evita registrar dos veces al mismo alumno en el mismo día
        unique_together = ['alumno', 'fecha']


# ─────────────────────────────────────────
# MODELO: Pago
# ─────────────────────────────────────────
class Pago(models.Model):

    MES_CHOICES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'),
        (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
        (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'),
        (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'),
    ]

    alumno     = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='pagos')
    monto      = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pago = models.DateField(auto_now_add=True)
    mes        = models.PositiveIntegerField(choices=MES_CHOICES)
    anio       = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.alumno.nombre} — {self.get_mes_display()} {self.anio}"

    class Meta:
        ordering = ['-anio', '-mes']
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        # Un alumno no puede pagar dos veces el mismo mes del mismo año
        unique_together = ['alumno', 'mes', 'anio']
