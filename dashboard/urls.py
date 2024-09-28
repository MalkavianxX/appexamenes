from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    #vistas render
    path('/view_dashboard',views.view_dashboard, name='view_dashboard'),

    #vistas render admin
    path('view_admin_est_alumnos',views.view_admin_est_alumnos, name='view_admin_est_alumnos'),
    path('views_admin_est_contenido',views.views_admin_est_contenido, name='views_admin_est_contenido'),
    path('views_invitations',views.views_invitations, name="views_invitations"),
    
    #funciones del sistema
    path('fun_generar_link', views.fun_generar_link, name="fun_generar_link"),
    path('enviar_comentario', views.enviar_comentario, name="enviar_comentario"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)