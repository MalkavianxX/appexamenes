from django.shortcuts import render

# Create your views here.
def view_examenes(request):
    return render(request, 'view_examenes.html')