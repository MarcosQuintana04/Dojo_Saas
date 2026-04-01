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
        # Para MMA niveles
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
    fecha_ingreso = models.DateField()
    activo       = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_disciplina_display()})"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'