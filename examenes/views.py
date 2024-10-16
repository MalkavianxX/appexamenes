from django.shortcuts import render
from .models import Examen, Pregunta, Respuesta, Categoria
from dashboard.models import MiExamen,MiPerfil
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404

import random
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def view_examenes(request):
    return render(request, 'view_examenes.html')

def eliminar_dolares():
    # Filtrar las preguntas de la categoría de Matemáticas
    cat = Categoria.objects.get(pk = 37)
    preguntas_matematicas = Pregunta.objects.filter(category=cat)
    
    for pregunta in preguntas_matematicas:
        # Eliminar todos los '$$' del texto de la pregunta
        
        pregunta.text = pregunta.text.replace("ewline", '\newline')
        
        pregunta.save()
    print("eliminacion exitosa")
def view_config_examenes(request):
    categorias = Categoria.objects.all().exclude(name = "Simulador")
    examenes = [Examen.objects.filter(category=categoria) for categoria in categorias]
  
    
    print(examenes)
    return render(request, 'examenes/view_config_examenes.html',{'categorias_examenes': zip(categorias, examenes)})

def view_start_test(request, id, numpreguntas):
    examen = Examen.objects.get(pk=id)
    numpreguntas = int(numpreguntas)
    
    # Obtén todas las preguntas del examen y selecciona aleatoriamente el número especificado
    preguntas = list(examen.asks.all())
    preguntas_aleatorias = random.sample(preguntas, min(numpreguntas, len(preguntas)))
    count = 1

    # Obtén las respuestas para cada pregunta seleccionada
    preguntas_con_respuestas = {}
    for pregunta in preguntas_aleatorias:
        pregunta.num_pregunta = count
        respuestas = pregunta.respuesta_set.all()
        preguntas_con_respuestas[pregunta] = respuestas
        count = count + 1
    return render(request, 'examenes/start_examen.html', {
        'examen': examen,
        'preguntas_con_respuestas': preguntas_con_respuestas,
        'numpreguntas':numpreguntas,
    })


def evaluar_examen(request,id_examen, respuestas_dict,tiempo_examen,estado,tiempos_ans, numpreguntas):
    tiempo_usado =  float(tiempo_examen)/60
    
    # Conversión a minutos con parte decimal
    minutos_con_decimal = float(tiempo_examen / 60)

    # Obtener la parte entera de los minutos (sin usar math)
    minutos_completos = int(minutos_con_decimal)

    # Calcular los segundos restantes
    segundos_restantes = (minutos_con_decimal - minutos_completos) * 60
  

    tiempo_usado = float(str(minutos_completos)+ "." + str(round(segundos_restantes)))

    # Obtener el examen
    examen = get_object_or_404(Examen, id=id_examen)

    # Crear una instancia de MiExamen
    mi_examen = MiExamen(
        user=request.user,  # Asegúrate de que estás manejando el usuario correctamente
        test=examen,
        time = tiempo_usado
    )

    # Guardar la instancia de MiExamen en la base de datos
    mi_examen.save()

    # Inicializar variables para el cálculo de la calificación y el tiempo total
    total_preguntas = int(numpreguntas)
    respuestas_correctas = 0
  

    for id_pregunta, id_respuesta in respuestas_dict.items():
        # Obtener la pregunta y la respuesta seleccionada
        
        respuesta = get_object_or_404(Respuesta, id=id_respuesta)

        # Verificar si la respuesta es correcta
        if respuesta.correct:
            respuestas_correctas += 1

        print("pregunta evaluada")

        # Asociar la respuesta a la instancia de MiExamen
        mi_examen.asnwers.add(respuesta)

    # Calcular la calificación (puedes personalizar esto según tus necesidades)
    calificacion = (respuestas_correctas / total_preguntas) * 10.0

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
        tiempo_usado_segundos = data.get('tiempoRestante', 0)
        numpreguntas = data.get('numpreguntas',0)

        print(id_examen)
        print(respuestas)
        print(tiempos)
        print(termino)
        print(tiempo_usado_segundos)
        print(numpreguntas)
  
        miexamen = evaluar_examen(request,id_examen,respuestas,tiempo_usado_segundos,termino,tiempos, numpreguntas)

        return JsonResponse(data= {'mensaje': 'Datos recibidos correctamente','miexamen_id': miexamen.id})
   
    else:
        return JsonResponse(data= {'error': 'Método no permitido'}, status=400)
    


def view_result_examen(request, id_miexamen):
    # Obtén la instancia de MiExamen usando el ID
    mi_examen = MiExamen.objects.select_related('test').prefetch_related('asnwers__ask').get(id=id_miexamen)
    mi_examen.time = float(mi_examen.time)
    tiempo = "{:.2f} minutos".format(mi_examen.time)

    # Información que enviarás a la plantilla
    resumen_data = {
        'examen_resultado': mi_examen.score,
        'titulo_examen': mi_examen.test.title,
        'num_preguntas': mi_examen.asnwers.count(),
        'tiempo_total': tiempo,
        'prc_preguntas': 0.0,  # Porcentaje de preguntas respondidas
        'prc_tiempo': 0.0,  # Porcentaje de tiempo utilizado
        'resultados': [],
        'correctas':0,
        'incorrectas':0
    }

    # Obtener todas las respuestas correctas de una vez
    respuestas_correctas_dict = {respuesta.ask_id: respuesta.text for respuesta in Respuesta.objects.filter(correct=True)}
    correctas = 0
    incorrectas = 0
    # Itera sobre las preguntas del examen
    for count, item in enumerate(mi_examen.asnwers.all(), start=1):
        pregunta = item.ask

        # Agrega detalles de la pregunta al resumen_data
        if item.correct:
            respuesta_correcta = item.text
            resultado = "Correcto"
            correctas = correctas + 1
        else:
            respuesta_correcta = respuestas_correctas_dict.get(pregunta.id, "No disponible")
            resultado = "Incorrecto"
            incorrectas = incorrectas + 1
        resumen_data['correctas'] = correctas
        resumen_data['incorrectas'] = incorrectas
        resumen_data['resultados'].append({
            'numero_pregunta': count,
            'texto_pregunta': pregunta.text,
            'texto_respuesta_seleccionada': item.text,
            'texto_respuesta_correcta': respuesta_correcta,
            'resultado': resultado
        })
    if int(resumen_data['num_preguntas']) > 0:
        resumen_data['prc_preguntas'] = "{:.2f}".format((int(resumen_data['incorrectas']) + int(resumen_data['correctas'])) / int(resumen_data['num_preguntas']) * 100 )
        resumen_data['prc_tiempo'] = "{:.2f}".format((mi_examen.time / int(resumen_data['num_preguntas']))*100)
    else:
        resumen_data['prc_preguntas'] = 0   
        resumen_data['prc_tiempo'] = 0
    return render(request, "examenes/view_result_examen.html", {'resumen_data': resumen_data}) 


def view_test_complete(request):

    # Obtén todos los exámenes realizados
    examenes_realizados = MiExamen.objects.filter(user = request.user).order_by('-date')

    # Lista para almacenar la información de cada examen
    lista_examenes_info = []
   
    # Itera sobre cada examen y agrega la información relevante a la lista
    for examen in examenes_realizados:
        examen.time = float(examen.time)
        if examen.time < 1:
            tiempo = "{:.2f} segundos".format(examen.time * 60)
        else:
            tiempo = "{:.2f} minutos".format(examen.time)
        examen_info = {
            'id':examen.id,
            'nombre_examen': examen.test.title,
            'calificacion': "{0:.2f}".format(examen.score),
            'estado': examen.status,
            'tiempo': tiempo ,
            'fecha': examen.date.strftime('%d-%m-%Y')
        }
        lista_examenes_info.append(examen_info)
    # Pasa la lista a la plantilla para su renderización
    return render(request, 'examenes/view_examenes_completados.html', {'examenes_realizados': lista_examenes_info})


def view_simulator_start(request):
    return render(request, 'examenes/simulator_view.html')


def fun_terminar_examen(request,id):
    examen = Examen.objects.get(pk = id)
    examen.delete()
    
