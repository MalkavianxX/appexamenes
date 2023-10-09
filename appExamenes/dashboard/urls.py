from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    #vistas render
    path('/view_dashboard',views.view_dashboard, name='view_dashboard'),

    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)