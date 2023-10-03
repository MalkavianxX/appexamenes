from django.shortcuts import render

# Create your views here.
def view_login(request):
    return render(request, 'login/login.html')

def view_signup(request):
    return render(request, 'login/signup.html')
