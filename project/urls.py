from project import models,views
from django.urls import path


app_name = 'project'

urlpatterns = [
	
		path(r'^dashboard/$', views.Dashboard.as_view(),name="dashboard"),
		path(r'^project/add/$', views.ProjectCreateView.as_view(),name='project_create'),
		path(r'^project/(?P<slug>[-\w]+)/update/$', views.ProjectUpdateView.as_view(),name='project_update'),
		path(r'^project/all/$', views.ProjectListView.as_view(),name='project_list'),
		path(r'^project/(?P<slug>[-\w]+)/view/$', views.ProjectDetailView.as_view(),name='project_detail'),
		path(r'^project/(?P<slug>[-\w]+)/delete/$', views.ProjectDeleteView.as_view(),name='project_delete'),
		path(r'^project/(?P<slug>[-\w]+)/start/$', views.startProject , name='project_start'),
  
		


		path('equipment/add', views.EquipmentCreateView.as_view(),name='equip_create'),
		path('equipment/<str:slug>/update/', views.EquipmentUpdateView.as_view(),name='equip_update'),
		path('equipment/all/', views.EquipmentListView.as_view(),name='equip_list'),
		path('equipment/<str:slug>/view/', views.EquipmentDetailView.as_view(),name='equip_detail'),
		path('equipment/<str:slug>/delete/', views.EquipmentDeleteView.as_view(),name='equip_delete'),


		path('usage/add/equipment', views.UsageCreateView.as_view(),name='usage_create'),
		path('usage/<int:pk>/update/equipment/', views.UsageUpdateView.as_view(),name='usage_update'),
		path('usage/all/equipment', views.UsageListView.as_view(),name='usage_list'),
		path('usage/<int:pk>/view/equipment/', views.UsageDetailView.as_view(),name='usage_detail'),
		path('usage/<int:pk>/delete/equipment/', views.UsageDeleteView.as_view(),name='usage_delete'),

		
]