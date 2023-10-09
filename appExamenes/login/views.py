from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from dashboard.views import view_dashboard 
import json

# Create your views here.
def view_login(request):
    return render(request, 'login/login.html')

def view_signup(request):
    return render(request, 'login/signup.html')

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

