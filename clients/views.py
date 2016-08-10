from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .forms import LoginForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

# Create your views here.
def show(request):
	return HttpResponse("Hola desde el cliente")


def login(request):
	message = None
	# nombre = "José"
	# edad = 17
	# context = { 'nombre' : nombre, 'edad' : edad }
	# return render(request, 'login.html', context)

	if request.method == 'POST':
		username_post = request.POST['username']
		password_post = request.POST['password']

		user = authenticate(username=username_post, password=password_post)

		if user is not None:
			login_django(request, user)
			return redirect('client:dashboard')
		else:
			message = "Nombre de usuario o password incorrecto"


	form = LoginForm()
	context = {
		'form' : form,
		'message' : message,
	}
	return render(request, 'login.html', context)

@login_required
def dashboard(request):
	return render(request, 'dashboard.html', {})

def logout(request):
	logout_django(request)
	return redirect('client:login')