from django.urls import path
from . import views

app_name = 'horarios'

urlpatterns = [
    path('',                                views.horario_semanal,           name='semanal'),
    path('nueva/',                          views.crear_clase,               name='crear'),
    path('<int:pk>/',                       views.detalle_clase,             name='detalle'),
    path('<int:pk>/editar/',                views.editar_clase,              name='editar'),
    path('<int:pk>/eliminar/',              views.eliminar_clase,            name='eliminar'),
    path('<int:pk>/inscribir/',             views.inscribir_alumno,          name='inscribir'),
    path('<int:pk>/desinscribir/<int:alumno_pk>/', views.desinscribir_alumno, name='desinscribir'),
    path('<int:pk>/asistencia/',            views.registrar_asistencia_clase, name='asistencia'),
]