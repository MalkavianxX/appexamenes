from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # vistas render
    path('view_admin_users',views.view_admin_users, name='view_admin_users'),
    path('view_my_perfil/<int:id>/',views.view_my_perfil, name="view_my_perfil"),
    path('view_test_complete_admin/<int:id>/', views.view_test_complete_admin, name="view_test_complete_admin"),

    #funciones
    path('fun_addUser',views.fun_addUser, name="fun_addUser"),
    path('fun_upDataUser',views.fun_upDataUser, name="fun_upDataUser"),
    path('fun_upProfileUser',views.fun_upProfileUser, name="fun_upProfileUser"),
    path('fun_changePassword',views.fun_changePassword, name="fun_changePassword"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)