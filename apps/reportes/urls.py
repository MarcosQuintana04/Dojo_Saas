from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('alumnos/',                   views.reporte_alumnos,          name='alumnos'),
    path('deudores/',                  views.reporte_deudores,         name='deudores'),
    path('pagos/<int:pk>/',            views.reporte_pagos_alumno,     name='pagos_alumno'),
    path('asistencias/<int:pk>/',      views.reporte_asistencias_alumno, name='asistencias_alumno'),
]