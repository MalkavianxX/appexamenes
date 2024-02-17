from django.contrib.auth import logout
from functools import wraps
from django.shortcuts import redirect

def verificar_sesion(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Comprueba si el usuario ha iniciado sesión
        if request.user.is_authenticated:
            # Comprueba si la sesión actual del usuario coincide con la última sesión registrada
            if request.user.last_session_key != request.session.session_key:
                # Si no coinciden, cierra la sesión actual
                logout(request)
                # Redirige al usuario a la página de inicio de sesión
                return redirect('view_login')
        return func(request, *args, **kwargs)
    return wrapper

