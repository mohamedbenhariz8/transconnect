from django.shortcuts import render
from .models import offre
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from django.urls import reverse_lazy
from .forms import OffreForm

class offres_list(ListView):
    model = offre
    template_name = 'offre/offres_list.html'
    context_object_name = 'offres'
class offres_detail(DetailView):
    model = offre
    template_name = 'offre/offres_detail.html'
    context_object_name = 'offre'
class offres_delete(DeleteView):
    model = offre
    template_name = 'offre/offres_confirm_delete.html'
    success_url = reverse_lazy('offres_list')
class offres_create(CreateView):
    model = offre
    template_name = 'offre/offres_form.html'
    success_url = reverse_lazy('offres_list')
    form_class = OffreForm
class offres_update(UpdateView):
    model = offre
    template_name = 'offre/offres_form.html'
    success_url = reverse_lazy('offres_list')
    form_class = OffreForm
