from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/')),
    path('login/',  auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alumnos/',     include('apps.alumnos.urls',     namespace='alumnos')),
    path('asistencias/', include('apps.asistencias.urls', namespace='asistencias')),
    path('pagos/',       include('apps.pagos.urls',       namespace='pagos')),
    path('dashboard/',   include('apps.dashboard.urls',   namespace='dashboard')),
    path('horarios/',    include('apps.horarios.urls',    namespace='horarios')),
    path('reportes/',    include('apps.reportes.urls',    namespace='reportes')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)