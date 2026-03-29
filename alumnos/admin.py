from django.contrib import admin
from .models import Alumno, Asistencia, Pago

admin.site.register(Alumno)
admin.site.register(Asistencia)
admin.site.register(Pago)

