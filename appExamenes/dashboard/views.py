from django.shortcuts import render
from .models import MiPerfil, MiExamen
from django.utils import timezone
from django.db import models
from login.models import User
from examenes.models import Categoria, Pregunta, Examen
from .fun_estats import obtener_dias_con_mas_examenes ,obtener_cantidad_usuarios_ultimos_7_dias,obtener_usuarios_mas_examenes
def contar_total_examenes_realizados():
    # Obtén la cantidad total de exámenes realizados
    total_examenes = MiExamen.objects.count()
    return total_examenes

def calcular_promedio_general():
    # Obtén todos los exámenes
    examenes = MiExamen.objects.all()

    # Calcula el promedio general de calificaciones
    promedio_general = examenes.aggregate(promedio=models.Avg('score'))['promedio']

    if promedio_general is not None:
        promedio_general = round(promedio_general)
    else:
        promedio_general = 0

    return promedio_general

def calcular_porcentaje_aprobacion():
    # Obtén el porcentaje de exámenes aprobados
    total_examenes = MiExamen.objects.count()
    aprobados = MiExamen.objects.filter(status='Aprobado').count()

    porcentaje_aprobacion = (aprobados / total_examenes) * 100 if total_examenes > 0 else 0.0

    return round(porcentaje_aprobacion, 1)

def calcular_porcentaje_reprobacion():
    # Obtén el porcentaje de exámenes reprobados
    total_examenes = MiExamen.objects.count()
    reprobados = MiExamen.objects.filter(status='Reprobado').count()

    porcentaje_reprobacion = (reprobados / total_examenes) * 100 if total_examenes > 0 else 0.0

    return round(porcentaje_reprobacion, 1)

#funciones admin
def contar_usuarios_no_staff():
    # Filtra los usuarios que no son parte del staff
    usuarios_no_staff = User.objects.filter(is_staff=False)

    # Cuenta la cantidad de usuarios no staff
    cantidad_usuarios = usuarios_no_staff.count()

    return cantidad_usuarios



def view_dashboard(request):
    if request.user.is_staff:

        data_general = {
            'usuarios_total': contar_usuarios_no_staff(),
            'examenes_realizados':contar_total_examenes_realizados(),
            'prom_general':calcular_promedio_general(),
            'prc_aprovacion':calcular_porcentaje_aprobacion(),
            'prc_reprobacion':calcular_porcentaje_reprobacion(),
            'numero_total_examenes': Examen.objects.count(),
            'numero_total_categorias': Categoria.objects.count(),
            'numero_total_preguntas': Pregunta.objects.count(),
            'numero_total_usuarios_staff': User.objects.filter(is_staff=True).count(),
        }

        return render(request, 'dashboard/admin/sumary-admin.html',{'data_general':data_general})
    else:

        miperfil = MiPerfil.objects.get(user=request.user)
        misexamenes = MiExamen.objects.filter(user=request.user).order_by('-date')[:4]

        for examen in misexamenes:
            # Obtener la fecha actual en el mismo formato que el examen.date
            now = timezone.now()
            examen.score = float("{0:.2f}".format(examen.score))
            # Calcular la diferencia de tiempo en días
            diferencia = now - examen.date

            # Añadir una nueva propiedad al examen con la leyenda deseada
            if diferencia.days == 0:
                examen.fecha_anotada = "Hoy"
            elif diferencia.days == 1:
                examen.fecha_anotada = "Ayer"
            else:
                examen.fecha_anotada = f"Hace {diferencia.days} días"

        return render(request, 'dashboard/sumary.html', {'miperfil': miperfil, 'misexamenes': misexamenes})

def view_admin_users(request):

    return render(request, 'dashboard/admin/users.html',{'users':User.objects.all().order_by('-id')})

def view_admin_est_alumnos(request):
    data_general = {
        'usuarios_total': contar_usuarios_no_staff(),
        'examenes_realizados':contar_total_examenes_realizados(),
        'prom_general':calcular_promedio_general()
    }
    print(data_general)
    stats_test_per_week = obtener_dias_con_mas_examenes()
    stats_user_per_week = obtener_cantidad_usuarios_ultimos_7_dias()
    stats_user_more_tess = obtener_usuarios_mas_examenes()
    print(stats_test_per_week)
    print(stats_user_per_week)
    print(stats_user_more_tess)
    return render(request, 'dashboard/admin/estadistica/alumnos.html')