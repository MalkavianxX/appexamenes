from datetime import datetime, timedelta
from django.db.models import Count
from dashboard.models import MiExamen
def obtener_dias_con_mas_examenes():
    # Obtener la lista de días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    # Obtener la cantidad de exámenes por día de la semana
    examenes_por_dia = MiExamen.objects.values('date__week_day').annotate(cantidad=Count('id'))

    # Crear un diccionario para almacenar la cantidad de exámenes por día
    examenes_por_dia_dict = {dia: 0 for dia in dias_semana}

    # Actualizar el diccionario con la cantidad correspondiente
    for examen in examenes_por_dia:
        dia_numero = examen['date__week_day']
        examenes_por_dia_dict[dias_semana[dia_numero - 1]] = examen['cantidad']

    # Devolver la lista de días con la cantidad de exámenes
    return [(dia, examenes_por_dia_dict[dia]) for dia in dias_semana]

def obtener_cantidad_usuarios_ultimos_7_dias():
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Obtener la fecha de hace 7 días
    fecha_hace_7_dias = fecha_actual - timedelta(days=7)

    # Obtener la cantidad de usuarios que han realizado al menos un examen en los últimos 7 días
    usuarios_ultimos_7_dias = MiExamen.objects.filter(date__gte=fecha_hace_7_dias).values('user').distinct().count()

    # Devolver la cantidad de usuarios
    return usuarios_ultimos_7_dias

def obtener_usuarios_mas_examenes():
    # Obtener los 10 usuarios que han hecho más exámenes
    usuarios_mas_examenes = MiExamen.objects.values('user__username').annotate(cantidad=Count('user')).order_by('-cantidad')[:10]

    # Devolver la lista de usuarios con la cantidad de exámenes
    return [(usuario['user__username'], usuario['cantidad']) for usuario in usuarios_mas_examenes]
