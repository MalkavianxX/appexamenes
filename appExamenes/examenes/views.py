from django.shortcuts import render

# Create your views here.
def view_examenes(request):
    return render(request, 'view_examenes.html')


def view_config_examenes(request):
    return render(request, 'examenes/view_config_examenes.html')


def view_start_test(request):
    return render(request, 'examenes/start_examen.html')