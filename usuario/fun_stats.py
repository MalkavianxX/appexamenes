from dashboard.fun_estats import *


def obtener_examenes_ultimos_siete_dias(user):
    # Obtener la fecha actual
    fecha_actual = datetime.today()
   
    # Calcular la fecha de inicio (hace 7 días)
    examenes_dias = []
 
    for i in range(7):
        
        cant_examenes = MiExamen.objects.filter(user = user ).filter(date__date = fecha_actual).count()
      
        fecha_actual = fecha_actual - timedelta(days = 1)
        examenes_dias.append((fecha_actual.strftime('%d-%m'),cant_examenes))
   

    return examenes_dias