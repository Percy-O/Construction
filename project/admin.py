from django.contrib import admin
from project import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Project)
admin.site.register(models.Equipment)