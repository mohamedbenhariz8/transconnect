from django.urls import path
from .views import *
urlpatterns = [
 path('expedition_list/',Expedition_list.as_view(),name='expedition_list'),
 path('expedition_detail/<int:pk>/',Expedition_detail.as_view(),name='expedition_detail'),
 path('expedition_delete/<int:pk>/',Expedition_delete.as_view(),name='expedition_delete'),
 path('expedition_create/',Expedition_create.as_view(),name='expedition_create'),
 path('expedition_update/<int:pk>/',Expedition_update.as_view(),name='expedition_update')
]
