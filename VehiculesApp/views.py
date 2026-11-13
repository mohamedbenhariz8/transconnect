from django.shortcuts import render
from .models import Vehicule
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .forms import VehiculeForm

class vehicules_list(ListView):
    model = Vehicule
    template_name = 'vehicule/vehicules_list.html'
    context_object_name = 'vehicules'
class vehicules_detail(DetailView):
    model = Vehicule
    template_name = 'vehicule/vehicules_detail.html'
    context_object_name = 'vehicule'
class vehicules_delete(DeleteView):
    model = Vehicule
    template_name = 'vehicule/vehicules_confirm_delete.html'
    success_url = reverse_lazy('vehicules_list')
class vehicules_create(CreateView):
    model = Vehicule
    template_name = 'vehicule/vehicules_form.html'
    success_url = reverse_lazy('vehicules_list')
    form_class = VehiculeForm
class vehicules_update(UpdateView):
    model = Vehicule
    template_name = 'vehicule/vehicules_form.html'
    success_url = reverse_lazy('vehicules_list')
    form_class = VehiculeForm
