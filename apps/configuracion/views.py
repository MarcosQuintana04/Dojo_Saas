from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ConfiguracionDojo
from .forms import ConfiguracionDojoForm


@login_required
def panel_configuracion(request):
    # Obtenemos o creamos la configuración
    config = ConfiguracionDojo.get()

    if request.method == 'POST':
        form = ConfiguracionDojoForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada correctamente.')
            return redirect('configuracion:panel')
    else:
        form = ConfiguracionDojoForm(instance=config)

    contexto = {
        'form': form,
        'config': config,
    }
    return render(request, 'configuracion/panel.html', contexto)
