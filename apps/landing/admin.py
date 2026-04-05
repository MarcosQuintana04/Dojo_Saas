from django.contrib import admin
from .models import FotoGaleria, Disciplina, InstructorInfo


@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activa']
    list_editable = ['orden', 'activa']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'activa']
    list_editable = ['orden', 'activa']


@admin.register(InstructorInfo)
class InstructorInfoAdmin(admin.ModelAdmin):
    pass
