from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from login.my_decorators import verificar_sesion
from login.models import User
from dashboard.models import MiExamen, MiPerfil
from django.utils import timezone  
from .fun_stats import obtener_examenes_ultimos_siete_dias as est1
import json
from django.contrib.auth import  get_user_model
from django.core.files.base import ContentFile
import base64
from django.shortcuts import get_object_or_404

@login_required
@verificar_sesion
def view_admin_users(request):

    return render(request, 'usuario/users.html',{'users':User.objects.all().order_by('-id')})

def view_my_perfil(request,id):
    if request.user.is_superuser or request.user.is_staff:
        user_obj = User.objects.get(pk = id)
    else:
        user_obj = request.user
    miperfil = MiPerfil.objects.get(user=user_obj)
    misexamenes = MiExamen.objects.filter(user=user_obj).order_by('-date')[:4]
 
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
    return render(request, 'usuario/my_profile.html',{
        'user':user_obj,
        'miperfil': miperfil, 
        'misexamenes': misexamenes,
        'data_general':json.dumps(dict(est1(user_obj)))})


@login_required
@verificar_sesion
def view_test_complete_admin(request,id):
    user = User.objects.get(pk = id)
    # Obtén todos los exámenes realizados
    examenes_realizados = MiExamen.objects.filter(user = user).order_by('-date')

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
    return render(request, 'usuario/view_examenes_completados.html', {'user':user, 'examenes_realizados': lista_examenes_info})


def fun_addUser(request):
    if request.method == 'POST':

        # obtener informacion
        user_name = request.POST['nameuser'] 
        mailuser = request.POST['mailuser']
        roluser = request.POST['roluser']
        passworduser = request.POST['passworduser']


        #crear el usuario
        User = get_user_model()
        user = User.objects.create_user(username=user_name, email=mailuser, password=passworduser)
        if int(roluser) == 0:
            user.is_staff = True
        elif int(roluser) == 1:
            user.is_superuser = True
        user.save()
        

    return redirect('view_admin_users')

def fun_upDataUser(request):
  
    if request.user.is_superuser or request.user.is_staff:
        user_obj = User.objects.get(pk = request.POST['iduser'])
    else:
        user_obj = request.user    
    user_obj.username = request.POST['nameuser'] 
    user_obj.first_name = request.POST['first_name']
    user_obj.last_name = request.POST['last_name']
    user_obj.email = request.POST['mailuser'] 
    user_obj.description = request.POST['descripcion']
    user_obj.save()

    return redirect('view_my_perfil', user_obj.id)

def fun_upProfileUser(request):
    if request.method == 'POST':
        user_id = request.POST.get('iduser')
        user = get_object_or_404(User, pk = user_id)
        color = request.POST.get('color')
        avatar = request.POST.get('avatar')

        # Si se proporcionó un color, actualiza el color del usuario
        if color:
            user.color = color

        # Si se proporcionó un avatar, actualiza el avatar del usuario
        if avatar:
            # Si el avatar es una imagen subida, conviértela a un archivo
            if avatar.startswith('data:image'):
                format, imgstr = avatar.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                user.icon.save('avatar.' + ext, data)
            else:
                user.icon = avatar

        user.save()

        return redirect('view_my_perfil', user_id)

    return JsonResponse({'status': 'error', 'message': 'Se esperaba una solicitud POST'}, status=400)

def fun_changePassword(request):
    if request.method == 'POST':

        user_id = request.POST.get('iduserpass')
        password = request.POST.get('password1')
        user = get_object_or_404(User, pk = user_id)
        user.set_password(password)
        user.save()
        
        return redirect('view_my_perfil', user_id)
