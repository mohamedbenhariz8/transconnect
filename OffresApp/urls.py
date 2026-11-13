from django.urls import path
from .views import *
urlpatterns = [
 path('offres_list/',offres_list.as_view(),name='offres_list'),
 path('offres_detail/<int:pk>/',offres_detail.as_view(),name='offres_detail'),
 path('offres_delete/<int:pk>/',offres_delete.as_view(),name='offres_delete'),
 path('offres_create/',offres_create.as_view(),name='offres_create'),
 path('offres_update/<int:pk>/',offres_update.as_view(),name='offres_update')
]
