# alumnos/urls.py

from django.urls import path
from . import views  # el punto significa "desde esta misma app"

# "app_name" nos permite hacer referencia a estas URLs por nombre
# desde cualquier parte del proyecto, sin hardcodear la ruta.
# Por ejemplo: {% url 'alumnos:lista' %} en vez de escribir '/alumnos/'
app_name = 'alumnos'

urlpatterns = [

    # ── Alumnos ──────────────────────────────
    path('',                        views.lista_alumnos,      name='lista'),
    path('<int:pk>/',               views.detalle_alumno,     name='detalle'),
    path('nuevo/',                  views.crear_alumno,       name='crear'),
    path('<int:pk>/editar/',        views.editar_alumno,      name='editar'),
    path('<int:pk>/eliminar/',      views.eliminar_alumno,    name='eliminar'),

    # ── Asistencias ──────────────────────────
    path('asistencias/',            views.asistencias_hoy,    name='asistencias_hoy'),
    path('asistencias/nueva/',      views.registrar_asistencia, name='registrar_asistencia'),
    path('asistencias/<int:pk>/',   views.historial_asistencia, name='historial_asistencia'),

    # ── Pagos ────────────────────────────────
    path('pagos/deudores/',         views.deudores,           name='deudores'),
    path('pagos/nuevo/',            views.registrar_pago,     name='registrar_pago'),
    path('pagos/<int:pk>/',         views.historial_pagos,    name='historial_pagos'),
]