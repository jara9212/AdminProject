from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User

from .forms import LoginUserForm,CreateUserForm,EditUserForm,EditPasswordForm

from django.contrib.auth import authenticate,login as login_django,logout as logout_django,update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.views.generic import View,DetailView,CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

#mensajes con funciones
from django.contrib import messages
#mensajes con clases
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
"""
Clases 
"""
class ShowClass(DetailView):
	model = User
	template_name = 'show.html'
	#Filtrar por username ---Por default lo hace por el id--pk
	slug_field = 'username'
	#que atributo de la url
	slug_url_kwarg = 'username_url'

# def show(request):
# 	return HttpResponse("Hola desde el cliente")


class LoginClass(View):
	form = LoginUserForm()
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


class dashboardClass(LoginRequiredMixin, View):
	login_url = 'cliente:login'

	def get(self, request, *args, **kwargs):
		return render(request, 'dashboard.html', {})

# @login_required(login_url = 'client:login')
# def dashboard(request):
# 	return render(request, 'dashboard.html', {})



class CreateClass(CreateView):
	success_url = reverse_lazy('client:login')
	model = User
	template_name = 'create.html'
	form_class = CreateUserForm

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.set_password(self.object.password)
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())

# def create(request):
# 	form = CreateUserForm(request.POST or None)
# 	if request.method == 'POST':
# 		if form.is_valid():
# 			user = form.save(commit=false)
# 			user.set_password(user.password)
# 			user.save()
# 			return redirect('client:login')

# 	context = {
# 		'form' : form
# 	}
# 	return render(request, 'create.html', context)

class EditClass(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
	login_url = 'cliente:login'
	model = User
	template_name = 'edit.html'
	success_url = reverse_lazy('client:edit')
	form_class = EditUserForm
	success_message = "Tu usuario ha sido actualizado"

	def form_valid(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(EditClass, self).form_valid(request, *args, **kwargs)

	def get_object(self, queryset=None):
		return self.request.user



"""
Funciones
"""
@login_required( login_url = 'client:login' )
def edit_password(request):
	
	form = EditPasswordForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			current_password = form.cleaned_data['password']
			new_password = form.cleaned_data['new_password']

			if authenticate(username = request.user.username, password = current_password):
				request.user.set_password(  new_password )
				request.user.save()

				update_session_auth_hash( request, request.user )
				messages.success(request, 'password actualizado correctamente')
			else:
				messages.error(request, 'No es posible actualizar el password')

	context = {'form' : form }
	return render(request, 'edit_password.html', context)

				

@login_required( login_url = 'client:login' )
def logout(request):
	logout_django(request)
	return redirect('client:login')