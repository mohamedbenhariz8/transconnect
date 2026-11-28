from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from EntreprisesApp.mixins import (EntrepriseRequiseMixin, TransporteurRequisMixin,
                                   ChargeurRequisMixin, EntrepriseCouranteFormMixin)
from .forms import OffreForm
from .models import offre


class OffresVisiblesMixin:
    """Les prix sont confidentiels : un transporteur voit ses propres offres,
    un chargeur voit les offres recues sur ses expeditions."""
    def get_queryset(self):
        entreprise = self.get_entreprise()
        return (offre.objects
                .filter(Q(entreprise=entreprise) | Q(expedition__entreprise=entreprise))
                .select_related('expedition', 'entreprise', 'vehicule'))


class MesOffresModifiablesMixin:
    """Un transporteur ne modifie / retire que SES offres encore proposees (404 sinon)."""
    def get_queryset(self):
        return offre.objects.filter(entreprise=self.get_entreprise(), statut='proposee')


class OffreFormMixin:
    """Passe l'entreprise connectee au formulaire (filtrage des vehicules proposes)."""
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entreprise'] = self.get_entreprise()
        return kwargs


class offres_list(EntrepriseRequiseMixin, OffresVisiblesMixin, ListView):
    model = offre
    template_name = 'offre/offres_list.html'
    context_object_name = 'offres'


class offres_detail(EntrepriseRequiseMixin, OffresVisiblesMixin, DetailView):
    model = offre
    template_name = 'offre/offres_detail.html'
    context_object_name = 'offre'


class offres_delete(TransporteurRequisMixin, MesOffresModifiablesMixin, DeleteView):
    model = offre
    template_name = 'offre/offres_confirm_delete.html'
    success_url = reverse_lazy('offres_list')


class offres_create(TransporteurRequisMixin, EntrepriseCouranteFormMixin, OffreFormMixin, CreateView):
    model = offre
    template_name = 'offre/offres_form.html'
    success_url = reverse_lazy('offres_list')
    form_class = OffreForm

    def get_initial(self):
        # lien « Proposer une offre » depuis une expedition : ?expedition=<pk>
        initial = super().get_initial()
        if self.request.GET.get('expedition'):
            initial['expedition'] = self.request.GET['expedition']
        return initial


class offres_update(TransporteurRequisMixin, MesOffresModifiablesMixin, OffreFormMixin, UpdateView):
    model = offre
    template_name = 'offre/offres_form.html'
    success_url = reverse_lazy('offres_list')
    form_class = OffreForm


class OffreDecisionView(ChargeurRequisMixin, View):
    """Le chargeur proprietaire de l'expedition accepte ou refuse une offre proposee.
    POST uniquement : une action qui modifie un etat ne passe jamais par un GET."""
    http_method_names = ['post']
    nouveau_statut = None

    def post(self, request, pk):
        o = get_object_or_404(offre, pk=pk, statut='proposee', expedition__statut='publiee',
                              expedition__entreprise=self.get_entreprise())
        o.statut = self.nouveau_statut
        try:
            o.save()  # 'acceptee' : expedition attribuee + autres offres refusees (models.py)
            messages.success(request, f"Offre {o.get_statut_display().lower()}.")
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
        return redirect('offres_detail', pk=o.pk)


class offres_accepter(OffreDecisionView):
    nouveau_statut = 'acceptee'


class offres_refuser(OffreDecisionView):
    nouveau_statut = 'refusee'
