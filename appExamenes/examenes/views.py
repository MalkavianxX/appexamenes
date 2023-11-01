from django.shortcuts import render
from .models import Examen, Pregunta, Respuesta, Categoria
from dashboard.models import MiExamen,MiPerfil
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from login.my_decorators import verificar_sesion
from login.models import User


@login_required
@verificar_sesion
# Create your views here.
def view_examenes(request):
    return render(request, 'view_examenes.html')

@login_required
@verificar_sesion
def view_config_examenes(request):
    categorias = Categoria.objects.all()
    examenes = [Examen.objects.filter(category=categoria) for categoria in categorias]
    return render(request, 'examenes/view_config_examenes.html',{'categorias_examenes': zip(categorias, examenes)})

@login_required
@verificar_sesion
def view_start_test(request,id,numpreguntas):
    examen = Examen.objects.get(pk = id)
    # Obtén todas las preguntas con respuestas asociadas al examen
    preguntas_con_respuestas = {}

    for pregunta in examen.asks.all()[:int(numpreguntas)]:
        # Accede directamente a las respuestas de cada pregunta
        respuestas = pregunta.respuesta_set.all()

        # Agrega la pregunta y sus respuestas al diccionario
        preguntas_con_respuestas[pregunta] = respuestas
    return render(request, 'examenes/start_examen.html',{'examen': examen, 'preguntas_con_respuestas': preguntas_con_respuestas})

@login_required
@verificar_sesion
def evaluar_examen(request,id_examen, respuestas_dict,tiempo_examen,estado,tiempos_ans):
    """
        Evalúa un examen y guarda los resultados.

        :param request: El objeto de solicitud Django.
        :type request: django.http.HttpRequest
        :param id_examen: El ID del examen como cadena.
        :type id_examen: str
        :param respuestas_dict: Un diccionario con las respuestas del usuario.
        :type respuestas_dict: dict
        :param tiempo_examen: El tiempo total del examen en segundos como cadena.
        :type tiempo_examen: str
        :param estado: El estado de terminación del examen (hecho, agotado, error) como cadena.
        :type estado: str
        :return: Una instancia de la clase MiExamen que representa los resultados del examen.
        :rtype: MiExamen
        :param tiempos_ans: La lista de los tiempos que le tomo hacerlo
        :type tiempos_ans: list
    """
    print(estado)
    # Obtener el examen
    examen = get_object_or_404(Examen, id=id_examen)

    # Crear una instancia de MiExamen
    mi_examen = MiExamen(
        user=request.user,  # Asegúrate de que estás manejando el usuario correctamente
        test=examen,
        time = tiempo_examen
    )

    # Guardar la instancia de MiExamen en la base de datos
    mi_examen.save()

    # Inicializar variables para el cálculo de la calificación y el tiempo total
    total_preguntas = examen.asks.count()
    respuestas_correctas = 0
  

    for id_pregunta, id_respuesta in respuestas_dict.items():
        # Obtener la pregunta y la respuesta seleccionada
        pregunta = get_object_or_404(Pregunta, id=id_pregunta)
        respuesta = get_object_or_404(Respuesta, id=id_respuesta)

        # Verificar si la respuesta es correcta
        if respuesta.correct:
            respuestas_correctas += 1

   

        # Asociar la respuesta a la instancia de MiExamen
        mi_examen.asnwers.add(respuesta)

    # Calcular la calificación (puedes personalizar esto según tus necesidades)
    calificacion = (respuestas_correctas / total_preguntas) * 100.0

    # Asignar los valores calculados a la instancia de MiExamen
    mi_examen.score = calificacion

    mi_examen.status = determinar_estado(estado,calificacion)  # Debes definir la función determinar_estado

    mi_examen.save()
    # Llama a la función para actualizar el promedio general
    perfil_usuario = MiPerfil.objects.get(user=request.user)
    perfil_usuario.actualizar_promedio_general()
    perfil_usuario.actualizar_total_examenes()
    perfil_usuario.actualizar_estadisticas_examenes(mi_examen)
    return mi_examen

@login_required
@verificar_sesion
def determinar_estado(estado,calificacion):
    # Puedes personalizar esta función según tus criterios para determinar el estado del examen
    if estado == "agotado":
        return "Incompleto"
    if estado == "error":
        return "Error"
    if calificacion >= 60:
        return 'Aprobado'
    else:
        return 'Reprobado'

@login_required
@verificar_sesion
def evaluate_examan(request):
    if request.method == 'POST':
      
        # Obtener el cuerpo del JSON
        data = json.loads(request.body.decode('utf-8'))

        # Acceder a los datos
        id_examen = data['id_examen']
        respuestas = data.get('respuestas', [])
        tiempos = data.get('tiempos', [])
        termino = data.get('termino', '')
        tiempo_restante = data.get('tiempoRestante', 0)

        # Hacer lo que necesites con los datos (guardar en la base de datos, realizar cálculos, etc.)
        # Devolver una respuesta
        miexamen = evaluar_examen(request,id_examen,respuestas,tiempo_restante,termino,tiempos)

        return JsonResponse(data= {'mensaje': 'Datos recibidos correctamente','miexamen_id': miexamen.id})
   
    else:
        return JsonResponse(data= {'error': 'Método no permitido'}, status=400)
    
@login_required
@verificar_sesion
def view_result_examen(request,id_miexamen):
    # Obtén la instancia de MiExamen usando el ID
    mi_examen = MiExamen.objects.get(id=id_miexamen)

    # Información que enviarás a la plantilla
    resumen_data = {
        'examen_resultado': mi_examen.score,
        'titulo_examen': mi_examen.test.title,
        'num_preguntas': mi_examen.test.asks.count(),
        'tiempo_total': mi_examen.test.time,
        'prc_preguntas': 0.0,  # Porcentaje de preguntas respondidas
        'prc_tiempo': 0.0,  # Porcentaje de tiempo utilizado
        'resultados': []
    }

    # Itera sobre las preguntas del examen
    for idx, pregunta in enumerate(mi_examen.test.asks.all(), start=1):
        # Obtiene las respuestas seleccionadas por el usuario
        respuestas_seleccionadas = mi_examen.asnwers.filter(ask=pregunta)

        # Verifica si las respuestas seleccionadas son correctas
        respuestas_correctas = pregunta.respuesta_set.filter(correct=True)
        respuestas_correctas_ids = set(respuesta.id for respuesta in respuestas_correctas)
        respuestas_seleccionadas_ids = set(respuesta.id for respuesta in respuestas_seleccionadas)
        es_correcto = respuestas_correctas_ids == respuestas_seleccionadas_ids

        # Agrega detalles de la pregunta al resumen_data
        resumen_data['resultados'].append({
            'numero_pregunta': idx,
            'texto_pregunta': pregunta.text,
            'texto_respuesta_seleccionada': [respuesta.text for respuesta in respuestas_seleccionadas],
            'texto_respuesta_correcta': [respuesta.text for respuesta in respuestas_correctas],
            'resultado': 'Correcto' if es_correcto else 'Incorrecto' if respuestas_seleccionadas else 'Vacio'
        })

    # Calcula el porcentaje de preguntas respondidas
    prc_preguntas_respondidas = (len([r for r in resumen_data['resultados'] if r['resultado'] != 'Vacio']) / resumen_data['num_preguntas']) * 100
    resumen_data['prc_preguntas'] = round(prc_preguntas_respondidas, 2)

    # Calcula el porcentaje de tiempo utilizado
    tiempo_usado = float(mi_examen.time) / 1000  # Convierte de milisegundos a segundos
    prc_tiempo_usado = (tiempo_usado / float(mi_examen.test.time)) * 100
    resumen_data['prc_tiempo'] = round(prc_tiempo_usado, 2)

    return render(request,"examenes/view_result_examen.html",{'resumen_data': resumen_data})    



@login_required
@verificar_sesion
def view_test_complete(request):

    # Obtén todos los exámenes realizados
    examenes_realizados = MiExamen.objects.filter(user = request.user).order_by('-date')

    # Lista para almacenar la información de cada examen
    lista_examenes_info = []
   
    # Itera sobre cada examen y agrega la información relevante a la lista
    for examen in examenes_realizados:
        examen_info = {
            'id':examen.id,
            'nombre_examen': examen.test.title,
            'calificacion': "{0:.2f}".format(examen.score),
            'estado': examen.status,
            'tiempo': "{0:.2f} minutos".format( float(examen.test.time) - (int(examen.time)/60)) ,
            'fecha': examen.date.strftime('%d-%m-%Y')
        }
        lista_examenes_info.append(examen_info)
    # Pasa la lista a la plantilla para su renderización
    return render(request, 'examenes/view_examenes_completados.html', {'examenes_realizados': lista_examenes_info})

@login_required
@verificar_sesion
def view_simulator_start(request):
    return render(request, 'examenes/simulator_view.html')