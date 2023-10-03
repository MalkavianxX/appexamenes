from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    #vistas render
    path('',views.view_login, name='view_login'),
    path('signup',views.view_signup, name='view_signup'),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)