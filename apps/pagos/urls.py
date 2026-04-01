from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('',           views.deudores,           name='deudores'),
    path('nuevo/',     views.registrar_pago,     name='registrar'),
    path('<int:pk>/',  views.historial_pagos,    name='historial'),
]