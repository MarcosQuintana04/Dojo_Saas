import datetime
from io import BytesIO
from decimal import Decimal

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, HRFlowable
from reportlab.lib import colors

from apps.alumnos.models import Alumno
from apps.pagos.models import Pago
from apps.asistencias.models import Asistencia
from .utils import get_estilos, estilo_tabla, cabecera_reporte, COLOR_EXITO, COLOR_PELIGRO, COLOR_PRIMARIO


def generar_pdf(nombre_archivo):
    """
    Crea el buffer y el documento base.
    Devuelve (response, buffer, doc) listos para usar.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response, buffer, doc


# ─────────────────────────────────────────
# REPORTE 1: Lista de alumnos activos
# ─────────────────────────────────────────
@login_required
def reporte_alumnos(request):
    response, buffer, doc = generar_pdf('alumnos_activos.pdf')
    estilos = get_estilos()
    elements = []

    cabecera_reporte(elements, estilos, 'Lista de Alumnos Activos')

    alumnos = Alumno.objects.filter(activo=True).order_by('nombre')

    # Resumen
    elements.append(Paragraph(f'Total de alumnos activos: {alumnos.count()}', estilos['normal']))
    elements.append(Spacer(1, 12))

    # Tabla
    datos = [['#', 'Nombre', 'Disciplina', 'Cinturón', 'Teléfono', 'Ingreso']]
    for i, alumno in enumerate(alumnos, 1):
        datos.append([
            str(i),
            alumno.nombre,
            alumno.get_disciplina_display(),
            alumno.get_cinturon_display(),
            alumno.telefono,
            alumno.fecha_ingreso.strftime('%d/%m/%Y'),
        ])

    tabla = Table(datos, colWidths=[1*cm, 5*cm, 3*cm, 3*cm, 3*cm, 2.5*cm])
    tabla.setStyle(estilo_tabla())
    elements.append(tabla)

    doc.build(elements)
    response.write(buffer.getvalue())
    return response


# ─────────────────────────────────────────
# REPORTE 2: Deudores del mes
# ─────────────────────────────────────────
@login_required
def reporte_deudores(request):
    hoy = datetime.date.today()
    response, buffer, doc = generar_pdf(f'deudores_{hoy.strftime("%m_%Y")}.pdf')
    estilos = get_estilos()
    elements = []

    mes_nombre = hoy.strftime('%B %Y').capitalize()
    cabecera_reporte(elements, estilos, 'Reporte de Deudores', mes_nombre)

    alumnos_que_pagaron = Pago.objects.filter(
        mes=hoy.month,
        anio=hoy.year
    ).values_list('alumno_id', flat=True)

    deudores = Alumno.objects.filter(
        activo=True
    ).exclude(id__in=alumnos_que_pagaron).order_by('nombre')

    elements.append(Paragraph(
        f'Alumnos que no han pagado {mes_nombre}: {deudores.count()}',
        estilos['normal']
    ))
    elements.append(Spacer(1, 12))

    if deudores.exists():
        datos = [['#', 'Nombre', 'Disciplina', 'Teléfono']]
        for i, alumno in enumerate(deudores, 1):
            datos.append([
                str(i),
                alumno.nombre,
                alumno.get_disciplina_display(),
                alumno.telefono,
            ])

        tabla = Table(datos, colWidths=[1*cm, 7*cm, 4*cm, 5*cm])
        tabla.setStyle(estilo_tabla(color_header=COLOR_PELIGRO))
        elements.append(tabla)
    else:
        elements.append(Paragraph(
            f'¡Todos los alumnos han pagado {mes_nombre}!',
            estilos['centrado']
        ))

    doc.build(elements)
    response.write(buffer.getvalue())
    return response


# ─────────────────────────────────────────
# REPORTE 3: Historial de pagos de un alumno
# ─────────────────────────────────────────
@login_required
def reporte_pagos_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    response, buffer, doc = generar_pdf(f'pagos_{alumno.nombre.replace(" ", "_")}.pdf')
    estilos = get_estilos()
    elements = []

    cabecera_reporte(
        elements, estilos,
        f'Historial de Pagos',
        alumno.nombre
    )

    pagos = alumno.pagos.all()
    total = sum(p.monto for p in pagos) if pagos else Decimal('0')

    elements.append(Paragraph(f'Disciplina: {alumno.get_disciplina_display()}', estilos['normal']))
    elements.append(Paragraph(f'Total pagado: S/ {total}', estilos['normal']))
    elements.append(Spacer(1, 12))

    if pagos.exists():
        datos = [['Mes', 'Año', 'Monto', 'Fecha de pago']]
        for pago in pagos:
            datos.append([
                pago.get_mes_display(),
                str(pago.anio),
                f'S/ {pago.monto}',
                pago.fecha_pago.strftime('%d/%m/%Y'),
            ])

        # Fila de total
        datos.append(['', '', f'Total: S/ {total}', ''])

        tabla = Table(datos, colWidths=[4*cm, 3*cm, 4*cm, 4*cm])
        estilo = estilo_tabla(color_header=COLOR_EXITO)
        # Estilo especial para la fila de total
        estilo.add('FONTNAME',   (0, -1), (-1, -1), 'Helvetica-Bold')
        estilo.add('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d1e7dd'))
        tabla.setStyle(estilo)
        elements.append(tabla)
    else:
        elements.append(Paragraph('Sin pagos registrados.', estilos['centrado']))

    doc.build(elements)
    response.write(buffer.getvalue())
    return response


# ─────────────────────────────────────────
# REPORTE 4: Historial de asistencias de un alumno
# ─────────────────────────────────────────
@login_required
def reporte_asistencias_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    response, buffer, doc = generar_pdf(f'asistencias_{alumno.nombre.replace(" ", "_")}.pdf')
    estilos = get_estilos()
    elements = []

    cabecera_reporte(
        elements, estilos,
        'Historial de Asistencias',
        alumno.nombre
    )

    asistencias = alumno.asistencias.all()
    total = asistencias.count()
    presentes = asistencias.filter(presente=True).count()
    porcentaje = round((presentes / total * 100), 1) if total > 0 else 0

    elements.append(Paragraph(f'Total de clases: {total}', estilos['normal']))
    elements.append(Paragraph(f'Asistencias: {presentes}', estilos['normal']))
    elements.append(Paragraph(f'Porcentaje: {porcentaje}%', estilos['normal']))
    elements.append(Spacer(1, 12))

    if asistencias.exists():
        datos = [['Fecha', 'Estado', 'Observación']]
        for a in asistencias:
            datos.append([
                a.fecha.strftime('%d/%m/%Y'),
                'Presente' if a.presente else 'Ausente',
                a.observacion or '—',
            ])

        tabla = Table(datos, colWidths=[4*cm, 3*cm, 10*cm])
        estilo = estilo_tabla()

        # Colorear las celdas de estado
        for i, a in enumerate(asistencias, 1):
            color = COLOR_EXITO if a.presente else COLOR_PELIGRO
            estilo.add('TEXTCOLOR', (1, i), (1, i), color)
            estilo.add('FONTNAME',  (1, i), (1, i), 'Helvetica-Bold')

        tabla.setStyle(estilo)
        elements.append(tabla)
    else:
        elements.append(Paragraph('Sin asistencias registradas.', estilos['centrado']))

    doc.build(elements)
    response.write(buffer.getvalue())
    return response
