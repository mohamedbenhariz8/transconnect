from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from EntreprisesApp.mixins import ChargeurRequisMixin, EntrepriseCouranteFormMixin
from .forms import ExpeditionForm
from .models import expedition


class MesExpeditionsModifiablesMixin:
    """Un chargeur ne modifie / supprime que SES expeditions, et seulement tant qu'elles
    sont publiees (une expedition attribuee est engagee aupres d'un transporteur).
    Toute autre expedition est introuvable : 404."""
    def get_queryset(self):
        return expedition.objects.filter(entreprise=self.get_entreprise(), statut='publiee')


# lecture : publique
class Expedition_list(ListView):
    model = expedition
    template_name = 'expedition/list.html'
    context_object_name = 'liste'


class Expedition_detail(DetailView):
    model = expedition
    template_name = 'expedition/detail.html'
    context_object_name = 'exp'


class Expedition_delete(ChargeurRequisMixin, MesExpeditionsModifiablesMixin, DeleteView):
    model = expedition
    template_name = 'expedition/expedition_confirm_delete.html'
    success_url = reverse_lazy('expedition_list')


class Expedition_create(ChargeurRequisMixin, EntrepriseCouranteFormMixin, CreateView):
    model = expedition
    template_name = 'expedition/forms.html'
    success_url = reverse_lazy('expedition_list')
    form_class = ExpeditionForm


class Expedition_update(ChargeurRequisMixin, MesExpeditionsModifiablesMixin, UpdateView):
    model = expedition
    template_name = 'expedition/forms.html'
    success_url = reverse_lazy('expedition_list')
    form_class = ExpeditionForm
