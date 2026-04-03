# apps/reportes/utils.py

import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# Paleta de colores del sistema
COLOR_PRIMARIO  = colors.HexColor('#0d6efd')
COLOR_OSCURO    = colors.HexColor('#212529')
COLOR_GRIS      = colors.HexColor('#6c757d')
COLOR_CLARO     = colors.HexColor('#f8f9fa')
COLOR_EXITO     = colors.HexColor('#198754')
COLOR_PELIGRO   = colors.HexColor('#dc3545')


def get_estilos():
    """
    Devuelve un diccionario con los estilos reutilizables.
    Centralizarlos acá significa que si cambiás la tipografía
    o el color, se actualiza en todos los reportes.
    """
    styles = getSampleStyleSheet()

    estilos = {
        'titulo': ParagraphStyle(
            'titulo',
            fontSize=20,
            fontName='Helvetica-Bold',
            textColor=COLOR_OSCURO,
            spaceAfter=12,
        ),
        'subtitulo': ParagraphStyle(
            'subtitulo',
            fontSize=11,
            fontName='Helvetica',
            textColor=COLOR_GRIS,
            spaceAfter=2,
        ),
        'seccion': ParagraphStyle(
            'seccion',
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=COLOR_PRIMARIO,
            spaceBefore=12,
            spaceAfter=6,
        ),
        'normal': ParagraphStyle(
            'normal',
            fontSize=10,
            fontName='Helvetica',
            textColor=COLOR_OSCURO,
        ),
        'centrado': ParagraphStyle(
            'centrado',
            fontSize=10,
            fontName='Helvetica',
            alignment=TA_CENTER,
            textColor=COLOR_GRIS,
        ),
        'pie': ParagraphStyle(
            'pie',
            fontSize=8,
            fontName='Helvetica',
            textColor=COLOR_GRIS,
            alignment=TA_CENTER,
        ),
    }
    return estilos


def estilo_tabla(color_header=None):
    """
    Estilo base para todas las tablas del sistema.
    """
    if color_header is None:
        color_header = COLOR_PRIMARIO

    return TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), color_header),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 10),
        ('ALIGN',      (0, 0), (-1, 0), 'CENTER'),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        # Filas de datos
        ('FONTNAME',   (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',   (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_CLARO]),
        ('TOPPADDING',    (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        # Bordes
        ('GRID',      (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('LINEBELOW', (0, 0), (-1, 0),  1.5, color_header),
    ])


def cabecera_reporte(elements, estilos, titulo, subtitulo=None):
    elements.append(Paragraph('BERSERKER RONIN', ParagraphStyle(
        'dojo',
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=COLOR_PRIMARIO,
        spaceAfter=2,
    )))
    elements.append(Paragraph('Sistema de Gestión de Dojo', estilos['subtitulo']))
    elements.append(HRFlowable(width='100%', thickness=1.5, color=COLOR_PRIMARIO, spaceAfter=12))
    elements.append(Paragraph(titulo, estilos['titulo']))
    if subtitulo:
        elements.append(Paragraph(subtitulo, estilos['subtitulo']))
    elements.append(Spacer(1, 8))  # ← agregar este espaciado
    elements.append(Paragraph(
        f'Generado el {datetime.date.today().strftime("%d/%m/%Y")}',
        ParagraphStyle('fecha', fontSize=9, textColor=COLOR_GRIS, spaceAfter=16,
                       spaceBefore=8)  # ← agregar spaceBefore
    ))
    elements.append(Spacer(1, 8))