from django.contrib import admin
from .models import Universidad, MiExamen, MiPerfil, Invitation, Reporte

class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'gn_average_min', 'gn_average_max', 'gn_students', 'gn_success_st')
    search_fields = ['name', 'gn_average_min', 'gn_average_max', 'gn_students', 'gn_success_st']

class MiExamenAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'time', 'status', 'date')
    search_fields = ['user__username', 'test__title', 'score', 'time', 'status']

class MiPerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'average', 'total_test')
    search_fields = ['user__username', 'average', 'total_test']

class MiInviteAdmin(admin.ModelAdmin):
    list_display = ('status', 'code', 'admin','date_create','date_use','link')

class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comentario', 'fecha_up', 'fecha_re', 'visto', 'respuesta')
    list_filter = ('visto', 'fecha_up', 'fecha_re')
    search_fields = ('usuario__username', 'comentario', 'respuesta')
    date_hierarchy = 'fecha_up'
    ordering = ('-fecha_up',)
    def __str__(self):
        return str(self.comentario)
    
admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(MiExamen, MiExamenAdmin)
admin.site.register(MiPerfil, MiPerfilAdmin)
admin.site.register(Invitation,MiInviteAdmin)
admin.site.register(Reporte,ReporteAdmin)