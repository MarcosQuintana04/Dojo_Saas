import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PerfilAlumno
from .forms import CrearCuentaAlumnoForm


@login_required
def lista_cuentas(request):
    """Lista de alumnos con y sin cuenta."""
    perfiles = PerfilAlumno.objects.select_related('user', 'alumno')
    contexto = {
        'perfiles': perfiles,
        'total': perfiles.count(),
    }
    return render(request, 'portal_admin/lista_cuentas.html', contexto)


@login_required
def crear_cuenta(request):
    """Crear cuenta para un alumno."""
    if request.method == 'POST':
        form = CrearCuentaAlumnoForm(request.POST)
        if form.is_valid():
            alumno   = form.cleaned_data['alumno']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Crear el usuario de Django
            user = User.objects.create_user(
                username=username,
                password=password,
                email=alumno.email or ''
            )

            # Vincular con el alumno
            PerfilAlumno.objects.create(user=user, alumno=alumno)

            messages.success(
                request,
                f'Cuenta creada para {alumno.nombre}. '
                f'Usuario: {username}'
            )
            return redirect('portal_admin:lista_cuentas')
    else:
        form = CrearCuentaAlumnoForm()

    return render(request, 'portal_admin/crear_cuenta.html', {
        'form': form,
        'titulo': 'Crear cuenta de alumno'
    })


@login_required
def eliminar_cuenta(request, pk):
    """Eliminar cuenta de un alumno."""
    perfil = get_object_or_404(PerfilAlumno, pk=pk)
    if request.method == 'POST':
        nombre = perfil.alumno.nombre
        perfil.user.delete()  # elimina el User y en cascada el PerfilAlumno
        messages.success(request, f'Cuenta de {nombre} eliminada.')
        return redirect('portal_admin:lista_cuentas')
    return render(request, 'portal_admin/confirmar_eliminar.html', {'perfil': perfil})