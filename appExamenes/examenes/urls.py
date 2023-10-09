from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('view_config_examenes',views.view_config_examenes, name='view_config_examenes'),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)