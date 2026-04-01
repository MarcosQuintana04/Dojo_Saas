import datetime
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.alumnos.models import Alumno
from apps.pagos.models import Pago


@login_required
def dashboard(request):
    hoy = datetime.date.today()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Alumnos activos
    total_alumnos = Alumno.objects.filter(activo=True).count()

    # Deudores del mes
    alumnos_que_pagaron = Pago.objects.filter(
        mes=mes_actual,
        anio=anio_actual
    ).values_list('alumno_id', flat=True)

    total_deudores = Alumno.objects.filter(
        activo=True
    ).exclude(
        id__in=alumnos_que_pagaron
    ).count()

    # Ingresos del mes actual
    ingresos_mes = Pago.objects.filter(
        mes=mes_actual,
        anio=anio_actual
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    # Gráfico: últimos 6 meses
    meses_labels = []
    meses_ingresos = []

    for i in range(5, -1, -1):
        if mes_actual - i <= 0:
            mes = mes_actual - i + 12
            anio = anio_actual - 1
        else:
            mes = mes_actual - i
            anio = anio_actual

        nombre_mes = datetime.date(anio, mes, 1).strftime('%b %Y')
        meses_labels.append(nombre_mes)

        total = Pago.objects.filter(
            mes=mes,
            anio=anio
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

        meses_ingresos.append(float(total))

    contexto = {
        'total_alumnos': total_alumnos,
        'total_deudores': total_deudores,
        'ingresos_mes': ingresos_mes,
        'meses_labels': meses_labels,
        'meses_ingresos': meses_ingresos,
        'mes_actual': hoy.strftime('%B %Y'),
    }
    return render(request, 'dashboard/index.html', contexto)