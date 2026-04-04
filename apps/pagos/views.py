import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.alumnos.models import Alumno
from .models import Pago
from .forms import PagoForm
import urllib.parse 


@login_required
def registrar_pago(request):
    # Permitir pre-seleccionar un alumno desde la URL
    # ej: /pagos/nuevo/?alumno=5
    alumno_id = request.GET.get('alumno')
    alumno = None

    if alumno_id:
        from apps.alumnos.models import Alumno
        try:
            alumno = Alumno.objects.get(pk=alumno_id, activo=True)
        except Alumno.DoesNotExist:
            pass

    if request.method == 'POST':
        form = PagoForm(request.POST, alumno=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('pagos:deudores')
    else:
        form = PagoForm(alumno=alumno)
        # Pre-seleccionar el alumno en el selector
        if alumno:
            form.fields['alumno'].initial = alumno

    return render(request, 'pagos/form.html', {
        'form': form,
        'titulo': 'Registrar Pago'
    })


@login_required
def deudores(request):
    hoy = datetime.date.today()
    mes_nombre = hoy.strftime('%B %Y').capitalize()

    alumnos_que_pagaron = Pago.objects.filter(
        mes=hoy.month,
        anio=hoy.year
    ).values_list('alumno_id', flat=True)

    deudores = Alumno.objects.filter(
        activo=True
    ).exclude(id__in=alumnos_que_pagaron)

    al_dia = Alumno.objects.filter(
        activo=True,
        id__in=alumnos_que_pagaron
    )

    # Generamos el link de WhatsApp para cada deudor
    deudores_con_link = []
    for alumno in deudores:
        mensaje = (
            f'Hola {alumno.nombre.split()[0]} \U0001F44B\n\n'
            f'Te recordamos que tienes pendiente el pago '
            f'de *{mes_nombre}* en *Berserker Ronin*.\n'
            f'Por favor, acércate a regularizar tu situación.\n\n'
            f'*Este es un mensaje automatizado, si ya realizó el pago '
            f'o no continúa en la academia, ignore el mensaje.*\n\n'
            f'¡Gracias! \U0001F94B'
        )
        
        numero = alumno.telefono.strip().replace(' ', '')
        # Aseguramos que tenga código de país
        if not numero.startswith('+'):
            numero = f'51{numero}'  # código de Perú
        else:
            numero = numero.replace('+', '')
            
        mensaje_encoded = urllib.parse.quote(mensaje, safe='')
        link = f'https://wa.me/{numero}?text={mensaje_encoded}'
        
        deudores_con_link.append({
            'alumno': alumno,
            'link_whatsapp': link,
        })

    contexto = {
        'deudores_con_link': deudores_con_link,
        'al_dia': al_dia,
        'mes': mes_nombre,
        'total_deudores': deudores.count(),
        'total_al_dia': al_dia.count(),
    }
    return render(request, 'pagos/deudores.html', contexto)


@login_required
def historial_pagos(request, pk):
    from django.shortcuts import get_object_or_404
    alumno = get_object_or_404(Alumno, pk=pk)
    pagos = alumno.pagos.all()
    contexto = {
        'alumno': alumno,
        'pagos': pagos,
        'total_pagado': sum(p.monto for p in pagos),
    }
    return render(request, 'pagos/historial.html', contexto)