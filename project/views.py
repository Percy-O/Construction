from django.db.models import F
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.views.generic import CreateView,DeleteView,UpdateView,ListView,DetailView,RedirectView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404

from braces.views import SelectRelatedMixin


from project import models
from project import forms


# Create your views here.

###################################### Project Construction Operations #########################################

class Dashboard(LoginRequiredMixin,TemplateView):
	template_name = 'project/dashboard.html'
	
	login_url = '/login/'

class ProjectCreateView(LoginRequiredMixin,SelectRelatedMixin,CreateView):

	login_url = '/login/'
	fields = ['name','location','project_type','budget','sketch_project_image']
	model = models.Project

	# form_class = forms.ProjectForm
	
	template_name = 'project/project_form.html'

	# success_url = reverse_lazy('project_list')

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		project_image = self.request.FILES.get('sketch_project_image')
		self.object.sketch_project_image = project_image
		self.object.save()
		messages.success(self.request, 'Project Successfully Created!')
		return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin,UpdateView):

	login_url = '/login/'
	fields = ['name','project_type','budget','sketch_project_image']
	model = models.Project

	template_name ='project/project_form.html'

	def form_valid(self,form):
		self.object = form.save(commit=False)
		project_image = self.request.FILES.get('sketch_project_image')
		if project_image in self.request.FILES:
			self.object.sketch_project_image = project_image
		self.object.save()
		messages.success(self.request, 'Project Successfully Updated!')
		return super().form_valid(form)


class ProjectListView(LoginRequiredMixin,ListView):

	login_url = '/login/'
	model = models.Project
	template_name = 'project/project_list.html'

	def get_queryset(self):

		self.projects = models.Project.objects.select_related('user').filter(user=self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['projects']= self.projects
		return context

class ProjectDetailView(LoginRequiredMixin,DetailView):
	login_url = '/login/'
	model = models.Project


class ProjectDeleteView(LoginRequiredMixin,DeleteView):

	model = models.Project
	success_url = reverse_lazy('project:project_list')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id = self.request.user.id)

	def delete(self, *args, **kwargs):
		messages.success(self.request,'Project Deleted')
		return super().delete(*args, **kwargs)



def startProject(request,slug):

	project = get_object_or_404(models.Project,slug=slug)

	project.project_started()

	return redirect('project:project_list')


############################ Equipment ##################################



class EquipmentCreateView(LoginRequiredMixin,SelectRelatedMixin,CreateView):

	login_url = '/login/'
	fields = ['project','tool','quantity','price']
	select_related = ('user','project')
	model = models.Equipment
	template_name = 'project/equipment_form.html'

	def form_valid(self,form):
		self.object = form.save(commit=False)
		# getting the user
		self.object.user = self.request.user

		# getting the project object
		get_project = self.request.POST.get('project')
		project = get_object_or_404(models.Project,id=get_project)
		self.object.project = project
		self.object.save()
		messages.success(self.request, 'Equipment Successfully Added!')
		return super().form_valid(form)

class EquipmentUpdateView(LoginRequiredMixin,SelectRelatedMixin,UpdateView):

	login_url = '/login/'
	fields = ['tool','quantity','price']
	select_related = ('user','project')
	model = models.Equipment
	template_name = 'project/equipment_form.html'

	def form_valid(self,form):
		form.save(commit=True)
		messages.success(self.request, 'Equipment Successfully Updated!')
		return super().form_valid(form)


class EquipmentListView(LoginRequiredMixin,SelectRelatedMixin,ListView):

	login_url = '/login/'
	model = models.Equipment
	# select_related = ('user','project')
	template_name = 'project/equipment_list.html'

	def get_queryset(self):

		self.equipment = models.Equipment.objects.select_related('user','project').filter(user=self.request.user)

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['equipments'] = self.equipment
		return context

class EquipmentDetailView(LoginRequiredMixin,DetailView):
	login_url = '/login/'
	model = models.Equipment


class EquipmentDeleteView(LoginRequiredMixin,DeleteView):

	model = models.Equipment
	success_url = reverse_lazy('project:equip_list')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id = self.request.user.id)

	def delete(self, *args, **kwargs):
		messages.success(self.request,'Equipment Deleted')
		return super().delete(*args, **kwargs)


############################# Usage ###############################


class UsageCreateView(CreateView):
	
	model= models.EquipmentUsage
	fields = ['user','project','equipment','quantity']
	template_name = 'project/usage_form.html'

	def form_valid(self,form):
		self.object = form.save(commit=False)
		get_project = self.request.POST.get('project')
		get_equipment = self.request.POST.get('equipment')


		self.project = models.Project.objects.get(id=get_project)
		self.equipment = models.Equipment.objects.get(id=get_equipment)

		# New Quantity
		self.equipment.quantity -= int(self.object.quantity)
		self.equipment.save()

		# Passing the instance object
		self.object.equipment = self.equipment
		self.object.project = self.project

		self.object.save()
		messages.success(self.request, 'Project Equipment({}) Successfully Collected'.format(self.object.equipment.tool))
			

		# messages.error(self.request, 'Error Occur While Trying to Collect The Equipment({})'.format(self.object.equipment.tool))

		return super().form_valid(form)

	def form_invalid(self,*args,**kwargs):
		messages.error(self.request, 'Error Occur While Trying to Collect The Equipment({})'.format(self.equipment.tool))
		return super().form_invalid(*args,**kwargs)


class UsageUpdateView(UpdateView):
	
	model= models.EquipmentUsage
	fields = ['user','equipment','quantity']
	template_name = 'project/usage_form.html'

	def form_valid(self,form):
		self.object = form.save(commit=False)
		get_equipment = self.request.POST.get('equipment')

		# Getting the equipment instance
		self.equipment = models.Equipment.objects.get(id=get_equipment)

		# getting the usage instance
		self.usage = models.EquipmentUsage.objects.get(id=self.object.id)

		# print(self.object.quantity)
		# print(self.usage.quantity)

		# Getting the quantity if it is higher than the new quantity or not
		if self.usage.quantity > self.object.quantity:
			new_quantity = int(self.usage.quantity) - int(self.object.quantity)
			self.equipment.quantity += new_quantity

		elif self.usage.quantity < int(self.object.quantity):
			new_quantity = int(self.object.quantity) - int(self.usage.quantity) 
			self.equipment.quantity -= new_quantity

		self.equipment.save()


		self.object.save()
		messages.success(self.request, 'Project Equipment({}) Collected Successfully Update'.format(self.object.equipment.tool))
			

		return super().form_valid(form)

	def form_invalid(self,*args,**kwargs):
		messages.error(self.request, 'Error Occur While Trying to Update Collected Equipment({})'.format(self.equipment.tool))
		return super().form_invalid(*args,**kwargs)

class UsageListView(ListView):

	model = models.EquipmentUsage
	template_name = 'project/usage_list.html'
	context_object_name = 'usages'

	def get_queryset(self):
		self.usage = models.EquipmentUsage.objects.select_related('project','equipment').all()\
					.annotate(price=F('equipment__price')*F('quantity'))

		return self.usage


class UsageDetailView(LoginRequiredMixin,DetailView):
	login_url = '/login/'
	model = models.EquipmentUsage


class UsageDeleteView(LoginRequiredMixin,DeleteView):

	model = models.EquipmentUsage
	success_url = reverse_lazy('project:usage_list')
	context_object_name = 'usage'

	# def get_queryset(self):
	# 	queryset = super().get_queryset()
	# 	return queryset.filter(user_id = self.request.user.id)

	def delete(self, *args, **kwargs):
		messages.success(self.request,'Usage Equipment Deleted')
		return super().delete(*args, **kwargs)


