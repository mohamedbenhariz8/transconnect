from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from EntreprisesApp.mixins import TransporteurRequisMixin, EntrepriseCouranteFormMixin
from .forms import VehiculeForm
from .models import Vehicule


class VehiculesDeMonEntrepriseMixin:
    """Un transporteur ne touche qu'aux vehicules de son entreprise (404 sinon)."""
    def get_queryset(self):
        return Vehicule.objects.filter(entreprise=self.get_entreprise())


# lecture : publique
class vehicules_list(ListView):
    model = Vehicule
    template_name = 'vehicule/vehicules_list.html'
    context_object_name = 'vehicules'


class vehicules_detail(DetailView):
    model = Vehicule
    template_name = 'vehicule/vehicules_detail.html'
    context_object_name = 'vehicule'


class mes_vehicules(TransporteurRequisMixin, VehiculesDeMonEntrepriseMixin, vehicules_list):
    """Lien « Mes véhicules » de la barre de navigation (transporteur)."""
    extra_context = {'titre': 'Mes véhicules'}


class vehicules_delete(TransporteurRequisMixin, VehiculesDeMonEntrepriseMixin, DeleteView):
    model = Vehicule
    template_name = 'vehicule/vehicules_confirm_delete.html'
    success_url = reverse_lazy('vehicules_list')


class vehicules_create(TransporteurRequisMixin, EntrepriseCouranteFormMixin, CreateView):
    model = Vehicule
    template_name = 'vehicule/vehicules_form.html'
    success_url = reverse_lazy('vehicules_list')
    form_class = VehiculeForm


class vehicules_update(TransporteurRequisMixin, VehiculesDeMonEntrepriseMixin, UpdateView):
    model = Vehicule
    template_name = 'vehicule/vehicules_form.html'
    success_url = reverse_lazy('vehicules_list')
    form_class = VehiculeForm
