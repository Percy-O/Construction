from django import forms
from project import models
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from project import models


class RegisterUser(UserCreationForm):

	class Meta:

		# model = settings.AUTH_USER_MODEL
		model = models.User
		fields = ['first_name','last_name','company_name','username','email','password1','password2']

		def __init__(self,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.fields['email'].label = 'Company Email'
			self.fields['username'].label = 'Preffered Username'


class ProjectForm(forms.ModelForm):

	class Meta:

		model = models.Project
		fields=['name']
		# fields = ['name','location','project_type','sketch_project_image','budget']
