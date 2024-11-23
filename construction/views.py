from django.shortcuts import render
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages


from project import forms
#################### Registration, Login, Logout ####################################

class UserRegistration(CreateView):

	form_class = forms.RegisterUser
	success_url = reverse_lazy('login')

	template_name = 'register.html'

class Login(LoginView):

	template_name = 'login.html'

	def get_success_url(self):
		messages.success(self.request,'Successfully Login!')
		url = reverse_lazy('project:dashboard')
		return url

class Logout(LoginRequiredMixin,LogoutView):

	next_page = '/'


############################# Home Page ####################################

class Home(TemplateView):
	template_name = 'home.html'