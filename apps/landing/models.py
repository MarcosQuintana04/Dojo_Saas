from django.db import models


class FotoGaleria(models.Model):
    """Fotos para la galería de la landing."""
    titulo      = models.CharField(max_length=100, blank=True)
    imagen      = models.ImageField(upload_to='landing/galeria/')
    orden       = models.PositiveIntegerField(default=0)
    activa      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f'Foto {self.pk}'

    class Meta:
        ordering = ['orden', '-created_at']
        verbose_name = 'Foto de galería'
        verbose_name_plural = 'Fotos de galería'


class Disciplina(models.Model):
    """Disciplinas mostradas en la landing."""
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono       = models.CharField(
        max_length=50,
        default='bi-trophy',
        help_text='Clase de Bootstrap Icons, ej: bi-trophy'
    )
    orden       = models.PositiveIntegerField(default=0)
    activa      = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['orden']
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'


class InstructorInfo(models.Model):
    """
    Información del instructor — patrón Singleton
    igual que ConfiguracionDojo.
    """
    nombre      = models.CharField(max_length=100)
    bio         = models.TextField()
    foto        = models.ImageField(
        upload_to='landing/instructor/',
        blank=True,
        null=True
    )
    experiencia = models.CharField(
        max_length=100,
        blank=True,
        help_text='ej: 15 años de experiencia'
    )

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        instructor, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'nombre': 'Instructor',
                'bio': 'Instructor de Berserker Ronin.',
            }
        )
        return instructor

    class Meta:
        verbose_name = 'Información del instructor'
        verbose_name_plural = 'Información del instructor'
