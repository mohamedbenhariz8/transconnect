"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth.decorators import login_not_required
from django.views.generic import TemplateView
from EntreprisesApp.views import InscriptionView, ProfilView, ProfilUpdateView

urlpatterns = [
    # pages publiques (LoginRequiredMiddleware protege tout le reste)
    path('', login_not_required(TemplateView.as_view(template_name='home.html')), name='accueil'),
    path('inscription/', login_not_required(InscriptionView.as_view()), name='inscription'),
    path('admin/', admin.site.urls),
    # authentification : vues fournies par Django, directement a la racine :
    # /login/, /logout/, /password_change/, ...
    path('profil/', ProfilView.as_view(), name='profil'),
    path('profil/modifier/', ProfilUpdateView.as_view(), name='profil_modifier'),
    path('', include('django.contrib.auth.urls')),
    path('expedition/', include('ExpeditionsApp.urls')),
    path('entreprise/', include('EntreprisesApp.urls')),
    path('vehicule/', include('VehiculesApp.urls')),
    path('offre/', include('OffresApp.urls')),
]
