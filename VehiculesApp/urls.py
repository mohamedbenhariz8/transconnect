from django.urls import path
from .views import *
urlpatterns = [
 path('vehicules_list/',vehicules_list.as_view(),name='vehicules_list'),
 path('vehicules_detail/<int:pk>/',vehicules_detail.as_view(),name='vehicules_detail'),
 path('vehicules_delete/<int:pk>/',vehicules_delete.as_view(),name='vehicules_delete'),
 path('vehicules_create/',vehicules_create.as_view(),name='vehicules_create'),
 path('vehicules_update/<int:pk>/',vehicules_update.as_view(),name='vehicules_update')
]
