from django.shortcuts import render
from .models import Examen, Pregunta, Respuesta
from dashboard.models import MiExamen
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404

# Create your views here.
def view_examenes(request):
    return render(request, 'view_examenes.html')


def view_config_examenes(request):
    return render(request, 'examenes/view_config_examenes.html')


def view_start_test(request):
    examen = Examen.objects.get(pk = 1)
    # Obtén todas las preguntas con respuestas asociadas al examen
    preguntas_con_respuestas = {}

    for pregunta in examen.asks.all():
        # Accede directamente a las respuestas de cada pregunta
        respuestas = pregunta.respuesta_set.all()

        # Agrega la pregunta y sus respuestas al diccionario
        preguntas_con_respuestas[pregunta] = respuestas
    return render(request, 'examenes/start_examen.html',{'examen': examen, 'preguntas_con_respuestas': preguntas_con_respuestas})




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



    return mi_examen

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
        print(respuestas, tiempos, termino, tiempo_restante)
        # Devolver una respuesta
        miexamen = evaluar_examen(request,id_examen,respuestas,tiempo_restante,termino,tiempos)
        print(miexamen)
        print(miexamen.score)
        print(float(miexamen.time)/1000)
        print(miexamen.status)
        print(miexamen.asnwers.all())

        return JsonResponse(data= {'mensaje': 'Datos recibidos correctamente'})
   
    else:
        return JsonResponse(data= {'error': 'Método no permitido'}, status=400)