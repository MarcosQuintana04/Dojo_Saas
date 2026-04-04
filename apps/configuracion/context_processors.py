from .models import ConfiguracionDojo


def configuracion_dojo(request):
    """
    Inyecta la configuración del dojo en todos los templates.
    Así podés usar {{ config_dojo.nombre }} en cualquier template.
    """
    return {
        'config_dojo': ConfiguracionDojo.get()
    }