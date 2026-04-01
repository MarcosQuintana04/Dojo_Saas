import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.alumnos.models import Alumno
from .models import Asistencia
from .forms import AsistenciaForm


@login_required
def asistencias_hoy(request):
    hoy = datetime.date.today()
    asistencias = Asistencia.objects.filter(fecha=hoy).select_related('alumno')
    contexto = {
        'asistencias': asistencias,
        'hoy': hoy,
        'presentes': asistencias.filter(presente=True).count(),
        'ausentes': asistencias.filter(presente=False).count(),
    }
    return render(request, 'asistencias/hoy.html', contexto)


@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia registrada.')
            return redirect('asistencias:hoy')
    else:
        form = AsistenciaForm()
    return render(request, 'asistencias/form.html', {
        'form': form,
        'titulo': 'Registrar Asistencia'
    })


@login_required
def historial_asistencia(request, pk):
    from django.shortcuts import get_object_or_404
    alumno = get_object_or_404(Alumno, pk=pk)
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
    return render(request, 'asistencias/historial.html', contexto)