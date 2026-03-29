# alumnos/urls.py

from django.urls import path
from . import views  # el punto significa "desde esta misma app"

# "app_name" nos permite hacer referencia a estas URLs por nombre
# desde cualquier parte del proyecto, sin hardcodear la ruta.
# Por ejemplo: {% url 'alumnos:lista' %} en vez de escribir '/alumnos/'
app_name = 'alumnos'

urlpatterns = [
    path('',               views.lista_alumnos,   name='lista'),
    path('<int:pk>/',      views.detalle_alumno,  name='detalle'),
    path('nuevo/',         views.crear_alumno,    name='crear'),
    path('<int:pk>/editar/',   views.editar_alumno,   name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar'),
]