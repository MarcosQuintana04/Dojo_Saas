import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.alumnos.models import Alumno
from .models import Pago
from .forms import PagoForm


@login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('pagos:deudores')
    else:
        form = PagoForm()
    return render(request, 'pagos/form.html', {
        'form': form,
        'titulo': 'Registrar Pago'
    })


@login_required
def deudores(request):
    hoy = datetime.date.today()
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

    contexto = {
        'deudores': deudores,
        'al_dia': al_dia,
        'mes': hoy.strftime('%B %Y'),
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