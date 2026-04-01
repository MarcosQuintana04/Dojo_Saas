from django.urls import path
from . import views

app_name = 'asistencias'

urlpatterns = [
    path('',            views.asistencias_hoy,    name='hoy'),
    path('nueva/',      views.registrar_asistencia, name='registrar'),
    path('<int:pk>/',   views.historial_asistencia, name='historial'),
]