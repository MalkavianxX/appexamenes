from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    #vistas render
    path('/view_dashboard',views.view_dashboard, name='view_dashboard'),

    #vistas render admin
    path('view_admin_users',views.view_admin_users, name='view_admin_users'),
    path('view_admin_est_alumnos',views.view_admin_est_alumnos, name='view_admin_est_alumnos'),

    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)