from django.urls import path
from . import views_portal, views_admin

# URLs del portal del alumno
portal_patterns = [
    path('login/',       views_portal.portal_login,       name='login'),
    path('logout/',      views_portal.portal_logout,      name='logout'),
    path('',             views_portal.portal_inicio,      name='inicio'),
    path('asistencias/', views_portal.portal_asistencias, name='asistencias'),
    path('pagos/',       views_portal.portal_pagos,       name='pagos'),
    path('horario/',     views_portal.portal_horario,     name='horario'),
]

# URLs de gestión de cuentas (para el admin)
admin_patterns = [
    path('',                        views_admin.lista_cuentas,   name='lista_cuentas'),
    path('crear/',                  views_admin.crear_cuenta,    name='crear_cuenta'),
    path('<int:pk>/eliminar/',      views_admin.eliminar_cuenta, name='eliminar_cuenta'),
]