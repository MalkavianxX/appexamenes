from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from dashboard.models import Invitation
import json
from django.utils import timezone
from dashboard.models import MiPerfil
from django.contrib.auth import logout

# Create your views here.
def view_login(request):
    if request.user.is_authenticated:
        return redirect('view_dashboard')
    else:
        return render(request, 'login/login.html')

def view_signup(request,code):
    try:
        invitacion = Invitation.objects.get(code = str(code))
        print("contrado")
        if invitacion.status == False:
            return render(request, 'login/signup.html',{'invitacion':invitacion.id})
        else:
            return render(request, 'login/error_signup.html')
    except:
        return render(request, 'login/error_signup.html')

def function_login(request):
    if request.method == 'POST': 
        data = json.loads(request.body.decode('utf-8'))

        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.set_session_key(request.session.session_key)
            
            return JsonResponse(data={'mensaje': 'Inicio de sesion correcto'})

        else:
            return JsonResponse(data={'error': 'El correo o la contraseña no son validos'}, status=401)
    else:
        return JsonResponse(data={'error': 'Método no permitido'}, status=400)

def create_user(request):
    if request.method == 'POST':
        # obtener informacion
        nombre_completo = request.POST['fullname'] 
        apellidos = request.POST['apellidos']
        correo_electronico = request.POST['emailaddress']
        contrasena = request.POST['password']
        code = request.POST['code']

        # buscar y actualizar la invitacion
        invitacion = Invitation.objects.get(pk = code)
        invitacion.status = True
        invitacion.date_use = timezone.now()
        invitacion.save()
        if invitacion.status == True:
            # Autentica al usuario
            # Crea un nuevo usuario
            User = get_user_model()
            user = User.objects.create_user(username=correo_electronico, email=correo_electronico, password=contrasena)
            user.first_name = nombre_completo
            user.last_name = apellidos
            user.save()

            #actualizar el perfil
            my_perfil = MiPerfil.objects.get(user = user)
            my_perfil.invitation_code = invitacion
            my_perfil.save()

            #logear al usuario
            login(request, user)
            user.set_session_key(request.session.session_key)

            return redirect('view_dashboard')
        else:
            return render(request, 'login/error_signup.html')
    else:
        return render(request, 'login/error_signup.html')

def fun_logut(request):
    logout(request)
    return render(request, 'login/logout.html')