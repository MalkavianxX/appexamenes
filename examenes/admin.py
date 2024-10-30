from django.contrib import admin
from .models import Categoria, Pregunta, Respuesta, Examen

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ['name']

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'weight', 'date','answer')
    search_fields = ['text', 'category__name']

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct', 'ask', 'date')
    search_fields = ['text', 'ask__text']

class ExamenAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'time', 'date')
    search_fields = ['title', 'category__name']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta, RespuestaAdmin)
admin.site.register(Examen, ExamenAdmin)
