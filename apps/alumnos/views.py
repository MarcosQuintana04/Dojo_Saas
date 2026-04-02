import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno
from .forms import AlumnoForm


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
        form = AlumnoForm(request.POST, request.FILES)

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
        form = AlumnoForm(request.POST, request.FILES, instance=alumno)
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