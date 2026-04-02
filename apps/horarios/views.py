import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.asistencias.models import Asistencia
from apps.alumnos.models import Alumno
from .models import Clase, Inscripcion
from .forms import ClaseForm, InscripcionForm


@login_required
def horario_semanal(request):
    """
    Vista principal — muestra todas las clases organizadas por día.
    """
    # Traemos todas las clases ordenadas por día y hora
    clases = Clase.objects.prefetch_related('alumnos')
    # prefetch_related es como select_related pero para ManyToMany

    # Organizamos por día para mostrar el horario semanal
    dias = {
        0: {'nombre': 'Lunes',     'clases': []},
        1: {'nombre': 'Martes',    'clases': []},
        2: {'nombre': 'Miércoles', 'clases': []},
        3: {'nombre': 'Jueves',    'clases': []},
        4: {'nombre': 'Viernes',   'clases': []},
        5: {'nombre': 'Sábado',    'clases': []},
        6: {'nombre': 'Domingo',   'clases': []},
    }

    for clase in clases:
        dias[clase.dia]['clases'].append(clase)

    # Día actual para resaltarlo en el horario
    dia_hoy = datetime.date.today().weekday()  # 0=lunes, 6=domingo

    contexto = {
        'dias': dias,
        'dia_hoy': dia_hoy,
    }
    return render(request, 'horarios/semanal.html', contexto)


@login_required
def detalle_clase(request, pk):
    """
    Muestra los alumnos inscritos en una clase y permite inscribir nuevos.
    """
    clase = get_object_or_404(Clase, pk=pk)
    inscripciones = clase.inscripciones.select_related('alumno')
    form = InscripcionForm(clase=clase)

    contexto = {
        'clase': clase,
        'inscripciones': inscripciones,
        'form': form,
        'total': inscripciones.count(),
    }
    return render(request, 'horarios/detalle.html', contexto)


@login_required
def inscribir_alumno(request, pk):
    """
    Inscribe un alumno a una clase específica.
    """
    clase = get_object_or_404(Clase, pk=pk)

    if request.method == 'POST':
        form = InscripcionForm(clase=clase, data=request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            # commit=False nos da el objeto sin guardarlo todavía
            # así podemos agregarle la clase antes de guardar
            inscripcion.clase = clase
            inscripcion.save()
            messages.success(request, f'{inscripcion.alumno.nombre} inscrito correctamente.')
        else:
            messages.error(request, 'Error al inscribir. Verificá los datos.')

    return redirect('horarios:detalle', pk=pk)


@login_required
def desinscribir_alumno(request, pk, alumno_pk):
    """
    Elimina la inscripción de un alumno en una clase.
    """
    inscripcion = get_object_or_404(Inscripcion, clase_id=pk, alumno_id=alumno_pk)

    if request.method == 'POST':
        nombre = inscripcion.alumno.nombre
        inscripcion.delete()
        messages.success(request, f'{nombre} fue removido de la clase.')

    return redirect('horarios:detalle', pk=pk)


@login_required
def crear_clase(request):
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase creada correctamente.')
            return redirect('horarios:semanal')
    else:
        form = ClaseForm()
    return render(request, 'horarios/form.html', {'form': form, 'titulo': 'Nueva Clase'})


@login_required
def editar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase actualizada.')
            return redirect('horarios:detalle', pk=clase.pk)
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'horarios/form.html', {'form': form, 'titulo': 'Editar Clase'})


@login_required
def eliminar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if request.method == 'POST':
        clase.delete()
        messages.success(request, 'Clase eliminada.')
        return redirect('horarios:semanal')
    return render(request, 'horarios/confirmar_eliminar.html', {'clase': clase})


@login_required
def registrar_asistencia_clase(request, pk):
    """
    Registra asistencia para todos los alumnos de una clase de una vez.
    Muestra la lista de inscritos con un checkbox por alumno.
    """
    clase = get_object_or_404(Clase, pk=pk)
    hoy = datetime.date.today()
    alumnos_inscritos = clase.alumnos.filter(activo=True)

    if request.method == 'POST':
        # Los alumnos que marcamos como presentes vienen en el POST
        presentes_ids = request.POST.getlist('presentes')

        for alumno in alumnos_inscritos:
            presente = str(alumno.pk) in presentes_ids
            # update_or_create: si ya existe la asistencia la actualiza,
            # si no existe la crea — evita duplicados elegantemente
            Asistencia.objects.update_or_create(
                alumno=alumno,
                fecha=hoy,
                defaults={'presente': presente}
            )

        messages.success(request, f'Asistencia registrada para {clase.nombre}.')
        return redirect('horarios:detalle', pk=pk)

    # Para cada alumno, verificamos si ya tiene asistencia hoy
    alumnos_con_estado = []
    for alumno in alumnos_inscritos:
        asistencia_hoy = Asistencia.objects.filter(
            alumno=alumno,
            fecha=hoy
        ).first()
        alumnos_con_estado.append({
            'alumno': alumno,
            'presente': asistencia_hoy.presente if asistencia_hoy else True,
            'ya_registrado': asistencia_hoy is not None,
        })

    contexto = {
        'clase': clase,
        'alumnos_con_estado': alumnos_con_estado,
        'hoy': hoy,
    }
    return render(request, 'horarios/asistencia.html', contexto)
