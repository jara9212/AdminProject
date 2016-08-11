from django import forms
from django.contrib.auth.models import User

"""
Constants
"""
ERROR_MESSAGE_USER = {'required':'El nombre de usuario es obligatorio', 'unique':'Este username ya existe', 'invalid' : 'el username es incorrecto'}
ERROR_MESSAGE_EMAIL = {'required':'debes ingresar un email', 'invalid' : 'ingrese un correo valido'}
ERROR_MESSAGE_PASSWORD = {'required':'la contraseña es obligatoria'}


"""
Functions
"""
def must_be_gt(value_password):
	if len(value_password) < 5 :
		raise forms.ValidationError('el password debe contener por lo menos 5 caracteres')




""""
Class
"""

class LoginUserForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput())

class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USER)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages=ERROR_MESSAGE_PASSWORD)
	email = forms.CharField(error_messages=ERROR_MESSAGE_EMAIL)
	class Meta:
		model = User
		fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages=ERROR_MESSAGE_USER)
	email = forms.CharField(error_messages=ERROR_MESSAGE_PASSWORD)
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')


class EditPasswordForm(forms.Form):
	password = forms.CharField(max_length=20, widget=forms.PasswordInput())
	new_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators = [must_be_gt])
	repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators = [must_be_gt])

	# def clean_new_password(self):
	# 	value_password = self.cleaned_data['new_password']
	# 	if len(value_password) < 5 :
	# 		raise forms.ValidationError('el password debe contener por lo menos 5 caracteres')
	# 	value_password

	def clean(self):
		clean_data = super(EditPasswordForm, self).clean()

		password1 = clean_data.get('new_password')
		password2 = clean_data.get('repeat_password')

		if password1 != password2:
			raise forms.ValidationError('Las contraseñas no son iguales')