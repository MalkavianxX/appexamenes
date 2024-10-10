from django.shortcuts import render,redirect
from .models import MiPerfil, MiExamen, Invitation, Reporte
from django.utils import timezone
from django.db import models
from login.models import User
from .fun_estats import *
import json
from django.db.models import Count
import secrets
from django.core.files.base import ContentFile
from login.my_decorators import verificar_sesion
import pandas as pd
from examenes.models import Pregunta, Respuesta, Categoria, Examen
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def enviar_comentario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comentario = data.get('comentario', '')

            if comentario:
                reporte = Reporte.objects.create(
                    usuario=request.user,
                    comentario=comentario
                )
                return JsonResponse({'status': 'ok', 'message': 'Comentario enviado correctamente.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'El comentario no puede estar vacío.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al procesar los datos JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
    
def cargar_preguntas():
    print("Comenzando proceso")
    df = pd.read_excel("C:/Users/Admin/Downloads/MATE.xlsx")
    categoria_quimica = Categoria.objects.get(id=37)
    
    for index, row in df.iterrows():
        # Crear la pregunta
        print("\nPregunta: ", row['p'])
        
        pregunta = Pregunta.objects.create(
            category=categoria_quimica,
            text=row['p'],
            weight=1  # Puedes ajustar el peso según sea necesario
        )
        
        # Manejar la imagen si está presente
        if pd.notna(row['i']):
            image_data = row['i']
            pregunta.imgage.save(f"pregunta_{index}.png", ContentFile(image_data))
        
        # Crear las respuestas
        respuestas = ['a', 'b', 'c']
        for letra in respuestas:
            print("\tRespuesta: ", row[letra])
            Respuesta.objects.create(
                text=row[letra],
                correct=False,
                ask=pregunta
            )
        
        # Crear la respuesta correcta
        Respuesta.objects.create(
            text=row['r'],
            correct=True,
            ask=pregunta
        )
    
    print("Datos cargados exitosamente")

def crear_examen():
    cat = Categoria.objects.get(pk=36)
    preguntas = Pregunta.objects.filter(category=cat)
    
    # Crear el examen y guardarlo para obtener un ID
    nuevo_examen = Examen.objects.create(
        category=cat,
        title="Español",
        time=50.0
    )
    
    # Asignar las preguntas al examen
    nuevo_examen.asks.set(preguntas)
    
    # Guardar el examen con las preguntas asignadas
    nuevo_examen.save()
    
    print("Examen creado exitosamente con las preguntas asignadas")
def sincro():
    preguntas = Pregunta.objects.all().prefetch_related('respuesta_set')
    
    with transaction.atomic():
        for item in preguntas:
            print("\npregunta: ", item.text)
            respuesta_correcta = next((r for r in item.respuesta_set.all() if r.correct), None)
            if respuesta_correcta:
                item.answer = respuesta_correcta.text
                print("\trespuesta correcta:", respuesta_correcta.text)
                item.save()
                print("guardada")

   
def examenes_con_mas_respuestas_equivocadas():
    # Obtener los 10 exámenes con más respuestas equivocadas
    examenes_equivocados = MiExamen.objects.filter(asnwers__correct=False).values('test__title').annotate(cantidad=Count('asnwers__id')).order_by('-cantidad')[:10]

    # Devolver la lista de exámenes con la cantidad de respuestas equivocadas
    resultados = {examen['test__title']: examen['cantidad'] for examen in examenes_equivocados}
    return json.dumps(resultados) 

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

from django.shortcuts import get_object_or_404

def crear_examen(nombre_examen, categoria):
    print("Empezando a crear examen")
    """
    Creates an exam with all questions belonging to the specified category.

    Args:
        nombre_examen (str): The name of the exam to be created.
        categoria (Categoria): The category object to which the questions belong.

    Returns:
        Examen: The created exam object.

    Raises:
        django.core.exceptions.ObjectDoesNotExist: If the specified category is not found.
    """

    # Retrieve the category object
    categoria_obj = get_object_or_404(Categoria, pk=categoria)

    # Filter questions belonging to the category
    preguntas = Pregunta.objects.filter(category=categoria_obj)
    print("Preguntas: ", len(preguntas))
    # Create the exam object
    examen = Examen.objects.create(
        title=nombre_examen,
        category=categoria_obj,
        time=15.0,  # Adjust the default time as needed
    )

    # Add questions to the exam using ManyToManyField relationship
    examen.asks.add(*preguntas)
    print("examen creado")
    return examen

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




@verificar_sesion
def view_admin_est_alumnos(request):
    alumnos = MiPerfil.objects.all()
    data_general = {
        'usuarios_total': contar_usuarios_no_staff(),
        'examenes_realizados':contar_total_examenes_realizados(),
        'prom_general':calcular_promedio_general(),
        'examenes_por_dia':json.dumps(dict(obtener_examenes_ultimos_siete_dias())) ,
        'usuarios_activos':obtener_cantidad_usuarios_ultimos_7_dias()
    }
 
    return render(request, 'dashboard/admin/estadistica/alumnos.html',{
        'data_general':data_general,
        'usuarios_examenes':alumnos.order_by('-total_test')[:5],
        'usuariores_mejores':alumnos.order_by('-average')[:5],
        'usuarios_peores':alumnos.order_by('average')[:5]
        })
 

@verificar_sesion
def views_admin_est_contenido(request):
    categorias = Categoria.objects.all()
    examenes = Examen.objects.all()
    preguntas = Pregunta.objects.all()
    respuestas = Respuesta.objects.all()
    data_general = {
        'total_category': categorias.count(),
        'total_test': examenes.count(),
        'total_ask':preguntas.count(),
        'total_ans':respuestas.count(),
    }

    # Supongamos que tienes un modelo llamado Examen con un campo 'categoria'
    categorias_contadas = Examen.objects.values('category__name').annotate(num_examenes=Count('category'))

    # Ahora, convierte el resultado a un diccionario
    diccionario_categorias = {str(categoria["category__name"]): categoria['num_examenes'] for categoria in categorias_contadas}
    diccionario_categorias = json.dumps(diccionario_categorias)

    return render(request, 'dashboard/admin/estadistica/contenido.html',{
        'data_general':data_general,
        'categorias_label': diccionario_categorias,
        'examenes_respuestas_equivocadas':examenes_con_mas_respuestas_equivocadas(),
    })


def generar_clave():
    return secrets.token_hex(5)  # Genera una clave segura de 10 caracteres

def fun_generar_link(request):
    code = generar_clave()
    invitacion = Invitation(
        code = code,
        admin = request.user,
        link = 'https://starfish-app-clgkk.ondigitalocean.app/signup/' + str(code) +'/'
    )
    invitacion.save()
    return redirect('views_invitations')

def views_invitations(request):

    my_invitations = Invitation.objects.all().order_by('status')

    
    return render(request, 'dashboard/admin/invitaciones/invitation.html',{
        'inivitaciones': my_invitations,
    })




