from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
# Create your models here.

# Geting User Model
# User = get_user_model()

class User(AbstractUser):

	company_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255,unique=True)

class Project(models.Model):

	user = models.ForeignKey(User, related_name='project' ,on_delete=models.CASCADE)
	name = models.CharField(max_length=255,verbose_name='project_name',help_text='Your Project Name')
	location = models.CharField(max_length=255,help_text='Where is it located')
	project_type = models.CharField(max_length=255,help_text='What type of project is it?')
	created_at = models.DateTimeField(auto_now=True)
	start_at = models.DateTimeField(blank=True,null=True,)
	slug = models.SlugField(allow_unicode=True,unique=True)
	sketch_project_image = models.ImageField(upload_to='project_image',verbose_name='Architectural Design',null=True,blank='',help_text='Architectural Design Image for the Project')
	budget = models.DecimalField(max_digits=8,decimal_places=2,help_text='Your Budget Price for the Project')
	# equipment = models.ManyToManyField('Equipment',through='Equipment')


	def __str__(self):
		return str(self.name)

	# Overriding the SAVE method
	def save(self,*args,**kwargs):
		self.slug = slugify(self.name)
		# self.save()
		return super().save(*args,**kwargs)

	def project_started(self,*args,**kwargs):

		self.start_at = timezone.now()

		return super().save(*args,**kwargs)

	def get_absolute_url(self):

		url  = reverse('project:project_list')
		return url


class Equipment(models.Model):
	user = models.ForeignKey(User, related_name='equipment' ,on_delete=models.CASCADE)
	tool = models.CharField(max_length=255)
	quantity = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=6,decimal_places=2)
	project = models.ForeignKey(Project,related_name='equipment', on_delete=models.CASCADE)
	slug = models.SlugField(allow_unicode=True,unique=True)
	created_at = models.DateTimeField(auto_now=True)




	def __str__(self):
		return str(self.tool)

	# Overriding the SAVE method
	def save(self,*args,**kwargs):
		self.slug = slugify(self.tool)
		return super().save(*args,**kwargs)

	def get_absolute_url(self):
		url  = reverse('project:equip_list')
		return url

	class Meta:
		ordering = ['created_at']


class EquipmentUsage(models.Model):

	user = models.CharField(max_length=255)
	project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='usage')
	equipment = models.ForeignKey(Equipment, related_name='usage' ,on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now=True)
	collected_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return str(self.user)

	def get_absolute_url(self):
		url = reverse('project:usage_list')
		return url





