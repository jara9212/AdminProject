from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .forms import LoginForm,CreateUserForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def show(request):
	return HttpResponse("Hola desde el cliente")


class LoginView(View):
	form = LoginForm()
	message = None
	template = 'login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('client:dashboard')
		return render(request, self.template, self.get_context())


	def post(self, request, *args, **kwargs):
		username_post = request.POST['username']
		password_post = request.POST['password']

		user = authenticate(username=username_post, password=password_post)
		if user is not None:
			login_django(request, user)
			return redirect('client:dashboard')
		else:
			message = "Nombre de usuario o password incorrecto"
			return render(request, self.template, self.get_context())


	def get_context(self):
		return {'form':self.form, 'message':self.message}

		

# def login_en_funciones(request):
# 	if request.user.is_authenticated():
# 		return redirect('client:dashboard')
# 	message = None
# 	# nombre = "José"
# 	# edad = 17
# 	# context = { 'nombre' : nombre, 'edad' : edad }
# 	# return render(request, 'login.html', context)

# 	if request.method == 'POST':
# 		username_post = request.POST['username']
# 		password_post = request.POST['password']

# 		user = authenticate(username=username_post, password=password_post)

# 		if user is not None:
# 			login_django(request, user)
# 			return redirect('client:dashboard')
# 		else:
# 			message = "Nombre de usuario o password incorrecto"


# 	form = LoginForm()
# 	context = {
# 		'form' : form,
# 		'message' : message,
# 	}
# 	return render(request, 'login.html', context)


class dashboardView(LoginRequiredMixin, View):
	login_url = 'cliente:login'

	def get(self, request, *args, **kwargs):
		return render(request, 'dashboard.html', {})

# @login_required(login_url = 'client:login')
# def dashboard(request):
# 	return render(request, 'dashboard.html', {})


def logout(request):
	logout_django(request)
	return redirect('client:login')

def create(request):
	form = CreateUserForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save(commit=false)
			user.set_password(user.password)
			user.save()
			return redirect('client:login')

	context = {
		'form' : form
	}
	return render(request, 'create.html', context)