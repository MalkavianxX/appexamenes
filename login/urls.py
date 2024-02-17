from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    #vistas render
    path('',views.view_login, name='view_login'),
    path('signup/<str:code>/',views.view_signup, name='view_signup'),
    path('create_user',views.create_user, name='create_user'),
    #funciones js
    path('function_login',views.function_login, name="function_login"),
    path('fun_logut',views.fun_logut, name="fun_logut"),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)