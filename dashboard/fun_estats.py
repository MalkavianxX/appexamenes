from datetime import datetime, timedelta
from django.db.models import Count
from dashboard.models import MiExamen,MiPerfil
def obtener_examenes_ultimos_siete_dias():
    # Obtener la fecha actual
    fecha_actual = datetime.today()
   
    # Calcular la fecha de inicio (hace 7 días)
    examenes_dias = []
 
    for i in range(7):
        
        cant_examenes = MiExamen.objects.filter(date__date = fecha_actual).count()
      
        fecha_actual = fecha_actual - timedelta(days = 1)
        examenes_dias.append((fecha_actual.strftime('%d-%m'),cant_examenes))
   

    return examenes_dias

def obtener_cantidad_usuarios_ultimos_7_dias():
    # Obtener la fecha actual
    fecha_actual = datetime.today()

    # Obtener la fecha de hace 7 días
    fecha_hace_7_dias = fecha_actual - timedelta(days=7)
 
    # Obtener la cantidad de usuarios que han realizado al menos un examen en los últimos 7 días
    usuarios_ultimos_7_dias = MiExamen.objects.filter(date__gte=fecha_hace_7_dias).values('user').distinct().count()

    # Devolver la cantidad de usuarios
    return usuarios_ultimos_7_dias

def obtener_usuarios_mas_examenes():

    return MiPerfil.objects.all().order_by('total_test')[:5]
