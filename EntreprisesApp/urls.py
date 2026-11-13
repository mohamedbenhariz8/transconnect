from django.urls import path
from .views import *
urlpatterns = [
 path('entreprises_list/',entreprises_list.as_view(),name='entreprises_list'),
 path('entreprises_detail/<int:pk>/',entreprises_detail.as_view(),name='entreprises_detail'),
 path('entreprises_delete/<int:pk>/',entreprises_delete.as_view(),name='entreprises_delete'),
 path('entreprises_create/',entreprises_create.as_view(),name='entreprises_create'),
 path('entreprises_update/<int:pk>/',entreprises_update.as_view(),name='entreprises_update')
]