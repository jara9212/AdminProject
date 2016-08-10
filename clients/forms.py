from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput())

class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages={'required':'El nombre de usuario es obligatorio', 
		'unique':'Este username ya existe', 'invalid' : 'el username es incorrecto'})
	password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages={'required':'la contraseña es obligatoria'})
	email = forms.CharField(error_messages={'required':'debes ingresar un email', 'invalid' : 'ingrese un correo valido'})
	class Meta:
		model = User
		fields = ('username', 'password', 'email')


