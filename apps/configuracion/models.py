from django.db import models


class ConfiguracionDojo(models.Model):
    """
    Configuración global del dojo.
    Solo debe existir un registro — patrón Singleton.
    """
    nombre          = models.CharField(max_length=100, default='Berserker Ronin')
    telefono        = models.CharField(max_length=20, blank=True)
    direccion       = models.CharField(max_length=200, blank=True)
    mensaje_bienvenida = models.TextField(
        blank=True,
        default='¡Bienvenido a Berserker Ronin! Estamos felices de tenerte con nosotros.'
    )

    def __str__(self):
        return f'Configuración — {self.nombre}'

    def save(self, *args, **kwargs):
        """
        Sobrescribimos save para garantizar que solo exista un registro.
        Si ya existe uno, actualizamos ese en vez de crear uno nuevo.
        """
        self.pk = 1  # siempre el mismo ID
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        """
        Método de clase para obtener la configuración fácilmente
        desde cualquier parte del proyecto.
        Crea el registro por defecto si no existe.
        """
        config, _ = cls.objects.get_or_create(pk=1)
        return config

    class Meta:
        verbose_name = 'Configuración del Dojo'
        verbose_name_plural = 'Configuración del Dojo'
