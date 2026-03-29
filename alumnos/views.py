# alumnos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno, Asistencia, Pago
from .forms import AlumnoForm, AsistenciaForm, PagoForm  
import datetime
from django.db.models import Count

# ─────────────────────────────────────────
# VISTA 1: Lista de alumnos
# ─────────────────────────────────────────
@login_required
def lista_alumnos(request):
    # El ORM de Django: Alumno.objects.all() genera
    # SELECT * FROM alumnos_alumno ORDER BY nombre
    # (el ORDER BY viene del Meta.ordering que definimos en el modelo)
    alumnos = Alumno.objects.filter(activo=True)

    # Pasamos los datos al template dentro de un diccionario
    # llamado "contexto". El template puede acceder a cada clave.
    contexto = {
        'alumnos': alumnos,
        'total': alumnos.count(),
    }
    return render(request, 'alumnos/lista.html', contexto)


# ─────────────────────────────────────────
# VISTA 2: Detalle de un alumno
# ─────────────────────────────────────────
@login_required
def detalle_alumno(request, pk):
    # get_object_or_404 intenta buscar el alumno con ese pk.
    # Si no existe, devuelve automáticamente una página 404
    # en vez de un error feo. Siempre usá esto en vez de .get()
    alumno = get_object_or_404(Alumno, pk=pk)

    # Gracias al related_name que definimos, podemos acceder
    # a las asistencias y pagos del alumno directamente
    asistencias = alumno.asistencias.all()[:10]  # últimas 10
    pagos = alumno.pagos.all()

    contexto = {
        'alumno': alumno,
        'asistencias': asistencias,
        'pagos': pagos,
    }
    return render(request, 'alumnos/detalle.html', contexto)


# ─────────────────────────────────────────
# VISTA 3: Crear alumno
# ─────────────────────────────────────────
@login_required
def crear_alumno(request):
    # En Django, los formularios tienen dos estados:
    # GET  → el usuario llegó a la página por primera vez, mostrar form vacío
    # POST → el usuario envió el formulario, procesar los datos

    if request.method == 'POST':
        # Creamos el form con los datos que envió el usuario
        form = AlumnoForm(request.POST)

        if form.is_valid():
            # is_valid() valida automáticamente todos los campos
            # (que el email tenga @, que los números sean números, etc.)
            form.save()  # guarda en la base de datos
            messages.success(request, 'Alumno registrado correctamente.')
            return redirect('alumnos:lista')  # redirige a la lista
        # Si el form no es válido, vuelve a mostrarlo con los errores
    else:
        form = AlumnoForm()  # form vacío para GET

    return render(request, 'alumnos/form.html', {'form': form, 'titulo': 'Nuevo Alumno'})


# ─────────────────────────────────────────
# VISTA 4: Editar alumno
# ─────────────────────────────────────────
@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        # La diferencia con crear: le pasamos "instance=alumno"
        # para que Django sepa que está MODIFICANDO, no creando
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumno actualizado correctamente.')
            return redirect('alumnos:detalle', pk=alumno.pk)
    else:
        # El form se pre-rellena automáticamente con los datos del alumno
        form = AlumnoForm(instance=alumno)

    return render(request, 'alumnos/form.html', {'form': form, 'titulo': 'Editar Alumno'})


# ─────────────────────────────────────────
# VISTA 5: Eliminar alumno
# ─────────────────────────────────────────
@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        # En vez de borrar físicamente, lo marcamos como inactivo.
        # Esto se llama "soft delete" — los datos siguen en la BD
        # por si los necesitás después (historial de pagos, etc.)
        alumno.activo = False
        alumno.save()
        messages.success(request, f'{alumno.nombre} fue dado de baja.')
        return redirect('alumnos:lista')

    # GET: mostrar página de confirmación antes de eliminar
    return render(request, 'alumnos/confirmar_eliminar.html', {'alumno': alumno})


# ─────────────────────────────────────────
# ASISTENCIAS
# ─────────────────────────────────────────

@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asistencia registrada.')
            return redirect('alumnos:asistencias_hoy')
        # Si hay error de unique_together (alumno ya registrado ese día),
        # Django lo captura y lo muestra en el form automáticamente
    else:
        form = AsistenciaForm()

    return render(request, 'asistencias/form.html', {
        'form': form,
        'titulo': 'Registrar Asistencia'
    })


@login_required
def asistencias_hoy(request):
    hoy = datetime.date.today()

    # El doble guión bajo (__) en Django ORM significa "navegar por relación"
    # fecha__date=hoy → busca registros donde el campo "fecha" sea igual a hoy
    asistencias = Asistencia.objects.filter(fecha=hoy).select_related('alumno')

    # select_related es una optimización importante.
    # Sin él: Django hace 1 query para las asistencias + 1 query por cada
    # alumno que necesita mostrar (problema N+1).
    # Con él: Django hace 1 sola query con JOIN. Mucho más eficiente.

    contexto = {
        'asistencias': asistencias,
        'hoy': hoy,
        'presentes': asistencias.filter(presente=True).count(),
        'ausentes': asistencias.filter(presente=False).count(),
    }
    return render(request, 'asistencias/hoy.html', contexto)


@login_required
def historial_asistencia(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    asistencias = alumno.asistencias.all()  # ya ordenadas por -fecha del Meta

    # Calculamos estadísticas básicas
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


# ─────────────────────────────────────────
# PAGOS
# ─────────────────────────────────────────

@login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('alumnos:deudores')
    else:
        form = PagoForm()

    return render(request, 'pagos/form.html', {
        'form': form,
        'titulo': 'Registrar Pago'
    })


@login_required
def deudores(request):
    hoy = datetime.date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Aquí viene la lógica más interesante del sistema.
    # Queremos: alumnos activos que NO tienen pago este mes/año.

    # Paso 1: obtener los IDs de alumnos que SÍ pagaron este mes
    alumnos_que_pagaron = Pago.objects.filter(
        mes=mes_actual,
        anio=anio_actual
    ).values_list('alumno_id', flat=True)
    # values_list con flat=True devuelve una lista plana: [1, 3, 7, ...]
    # en vez de una lista de tuplas: [(1,), (3,), (7,), ...]

    # Paso 2: excluir esos IDs de los alumnos activos
    deudores = Alumno.objects.filter(
        activo=True
    ).exclude(
        id__in=alumnos_que_pagaron
    )
    # id__in=lista → equivale a SQL: WHERE id NOT IN (1, 3, 7)
    # El exclude() hace el NOT IN

    # Alumnos al día (los que sí pagaron)
    al_dia = Alumno.objects.filter(
        activo=True,
        id__in=alumnos_que_pagaron
    )

    contexto = {
        'deudores': deudores,
        'al_dia': al_dia,
        'mes': hoy.strftime('%B %Y'),  # "Marzo 2025"
        'total_deudores': deudores.count(),
        'total_al_dia': al_dia.count(),
    }
    return render(request, 'pagos/deudores.html', contexto)


@login_required
def historial_pagos(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    pagos = alumno.pagos.all()

    contexto = {
        'alumno': alumno,
        'pagos': pagos,
        'total_pagado': sum(p.monto for p in pagos),
    }
    return render(request, 'pagos/historial.html', contexto)
