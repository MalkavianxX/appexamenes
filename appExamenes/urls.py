
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('examenes', include('examenes.urls')),
    path('dashboard', include('dashboard.urls')),
    path('usuarios', include('usuario.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)