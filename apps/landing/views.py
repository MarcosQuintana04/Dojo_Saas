from django.shortcuts import render
from .models import FotoGaleria, Disciplina, InstructorInfo
from apps.configuracion.models import ConfiguracionDojo
from apps.horarios.models import Clase


def landing(request):
    config      = ConfiguracionDojo.get()
    instructor  = InstructorInfo.get()
    fotos       = FotoGaleria.objects.filter(activa=True)
    disciplinas = Disciplina.objects.filter(activa=True)

    # Horarios agrupados por día — reutilizamos lo que ya existe
    clases = Clase.objects.all().order_by('dia', 'hora_inicio')

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

    # Solo mostrar días que tienen clases
    dias_con_clases = {k: v for k, v in dias.items() if v['clases']}

    contexto = {
        'config':          config,
        'instructor':      instructor,
        'fotos':           fotos,
        'disciplinas':     disciplinas,
        'dias_con_clases': dias_con_clases,
    }
    return render(request, 'landing/index.html', contexto)
