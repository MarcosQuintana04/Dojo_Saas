import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PerfilAlumno


def portal_login(request):
    """Login exclusivo para alumnos."""
    # Si ya está logueado como alumno, mandarlo al portal
    if request.user.is_authenticated:
        try:
            request.user.perfil_alumno
            return redirect('portal:inicio')
        except:
            pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verificar que es un alumno, no el admin
            try:
                user.perfil_alumno  # tiene perfil de alumno
                login(request, user)
                return redirect('portal:inicio')
            except PerfilAlumno.RelatedObjectDoesNotExist:
                messages.error(request, 'Esta cuenta no corresponde a un alumno.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'portal/login.html')


def portal_logout(request):
    logout(request)
    return redirect('portal:login')


def requiere_alumno(view_func):
    """
    Decorador propio para las vistas del portal.
    Verifica que el usuario logueado sea un alumno,
    no el administrador.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('portal:login')
        try:
            request.user.perfil_alumno
        except PerfilAlumno.RelatedObjectDoesNotExist:
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@requiere_alumno
def portal_inicio(request):
    """Página principal del portal del alumno."""
    alumno = request.user.perfil_alumno.alumno
    hoy = datetime.date.today()

    # Últimas 5 asistencias
    asistencias_recientes = alumno.asistencias.all()[:5]

    # ¿Pagó este mes?
    pago_mes = alumno.pagos.filter(
        mes=hoy.month,
        anio=hoy.year
    ).first()

    # Clases inscritas
    clases = alumno.clases.all()

    # Estadísticas de asistencia
    total_asistencias = alumno.asistencias.count()
    presentes = alumno.asistencias.filter(presente=True).count()
    porcentaje = round((presentes / total_asistencias * 100), 1) if total_asistencias > 0 else 0

    contexto = {
        'alumno': alumno,
        'asistencias_recientes': asistencias_recientes,
        'pago_mes': pago_mes,
        'clases': clases,
        'total_asistencias': total_asistencias,
        'presentes': presentes,
        'porcentaje': porcentaje,
        'mes_actual': hoy.strftime('%B %Y').capitalize(),
    }
    return render(request, 'portal/inicio.html', contexto)


@requiere_alumno
def portal_asistencias(request):
    """Historial completo de asistencias del alumno."""
    alumno = request.user.perfil_alumno.alumno
    asistencias = alumno.asistencias.all()

    total = asistencias.count()
    presentes = asistencias.filter(presente=True).count()
    porcentaje = round((presentes / total * 100), 1) if total > 0 else 0

    contexto = {
        'alumno': alumno,
        'asistencias': asistencias,
        'total': total,
        'presentes': presentes,
        'porcentaje': porcentaje,
    }
    return render(request, 'portal/asistencias.html', contexto)


@requiere_alumno
def portal_pagos(request):
    """Historial de pagos del alumno."""
    alumno = request.user.perfil_alumno.alumno
    hoy = datetime.date.today()
    pagos = alumno.pagos.all()

    pago_mes_actual = pagos.filter(
        mes=hoy.month,
        anio=hoy.year
    ).first()

    contexto = {
        'alumno': alumno,
        'pagos': pagos,
        'pago_mes_actual': pago_mes_actual,
        'mes_actual': hoy.strftime('%B %Y').capitalize(),
        'total_pagado': sum(p.monto for p in pagos),
    }
    return render(request, 'portal/pagos.html', contexto)


@requiere_alumno
def portal_horario(request):
    """Clases en las que está inscrito el alumno."""
    alumno = request.user.perfil_alumno.alumno
    clases = alumno.clases.all().order_by('dia', 'hora_inicio')

    contexto = {
        'alumno': alumno,
        'clases': clases,
    }
    return render(request, 'portal/horario.html', contexto)