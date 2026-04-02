from django.db import models
from apps.alumnos.models import Alumno


class Clase(models.Model):

    DIAS_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    DISCIPLINA_CHOICES = [
        ('karate', 'Karate'),
        ('mma', 'MMA'),
        ('ambas', 'Ambas'),
    ]

    nombre      = models.CharField(max_length=100)  # ej: "Karate Principiantes"
    disciplina  = models.CharField(max_length=10, choices=DISCIPLINA_CHOICES)
    dia         = models.PositiveIntegerField(choices=DIAS_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin    = models.TimeField()
    # ManyToMany con tabla intermedia explícita
    # "through" le dice a Django que use Inscripcion como tabla del medio
    alumnos     = models.ManyToManyField(
        Alumno,
        through='Inscripcion',
        related_name='clases',
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} — {self.get_dia_display()} {self.hora_inicio.strftime('%H:%M')}"

    class Meta:
        ordering = ['dia', 'hora_inicio']
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'


class Inscripcion(models.Model):
    """
    Tabla intermedia entre Alumno y Clase.
    Además de guardar la relación, guarda cuándo se inscribió el alumno.
    Esto es lo que hace útil usar 'through' en vez del ManyToMany simple.
    """
    alumno             = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    clase              = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion  = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno.nombre} → {self.clase.nombre}"

    class Meta:
        # Un alumno no puede estar inscrito dos veces en la misma clase
        unique_together = ['alumno', 'clase']
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
