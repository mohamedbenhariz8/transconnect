from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, TemplateView

from .forms import EntrepriseForm, InscriptionForm, ProfilForm
from .mixins import EntrepriseRequiseMixin, SansEntrepriseRequisMixin
from .models import Entreprise


class MonEntrepriseMixin:
    """Seule l'entreprise geree par l'utilisateur connecte est modifiable (404 sinon)."""
    def get_queryset(self):
        return Entreprise.objects.filter(gerant=self.request.user)


class entreprises_list(ListView):
    model = Entreprise
    template_name = 'entreprise/entreprises_list.html'
    context_object_name = 'entreprises'


class entreprises_detail(DetailView):
    model = Entreprise
    template_name = 'entreprise/entreprises_detail.html'
    context_object_name = 'entreprise'


class entreprises_delete(EntrepriseRequiseMixin, MonEntrepriseMixin, DeleteView):
    model = Entreprise
    template_name = 'entreprise/entreprises_confirm_delete.html'
    success_url = reverse_lazy('entreprises_list')


class entreprises_create(SansEntrepriseRequisMixin, CreateView):
    model = Entreprise
    template_name = 'entreprise/entreprises_form.html'
    success_url = reverse_lazy('expedition_list')
    form_class = EntrepriseForm

    def form_valid(self, form):
        user = self.request.user

        form.instance.gerant = user
        response = super().form_valid(form)
        
        if user.role != 'admin' and user.role != self.object.type_entreprise:
            user.role = self.object.type_entreprise
            user.save(update_fields=['role', 'updated_at'])
        return response


class entreprises_update(EntrepriseRequiseMixin, MonEntrepriseMixin, UpdateView):
    model = Entreprise
    template_name = 'entreprise/entreprises_form.html'
    success_url = reverse_lazy('entreprises_list')
    form_class = EntrepriseForm


class ProfilView(LoginRequiredMixin, TemplateView):
    """Affiche le profil de l'utilisateur connecte (toujours lui-meme : aucun pk dans l'URL)."""
    template_name = 'comptes/profil.html'


class ProfilUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfilForm
    template_name = 'comptes/profil_form.html'
    success_url = reverse_lazy('profil')
    success_message = "Votre profil a été mis à jour."

    def get_object(self, queryset=None):
        return self.request.user


class InscriptionView(CreateView):
    form_class = InscriptionForm
    template_name = 'registration/inscription.html'
    success_url = reverse_lazy('entreprises_create')

    def form_valid(self, form):
        response = super().form_valid(form)   
        login(self.request, self.object)     
        return response
