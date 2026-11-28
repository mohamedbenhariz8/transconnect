from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


def entreprise_de(user):
    """Entreprise geree par l'utilisateur, ou None (visiteur anonyme ou compte sans entreprise)."""
    return getattr(user, 'entreprise', None)


class EntrepriseRequiseMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Reserve la vue a un utilisateur connecte qui gere une entreprise.

    type_requis : 'chargeur' ou 'transporteur' pour restreindre a un type d'entreprise.
    Anonyme -> redirection vers la connexion ; connecte sans le bon type -> 403.
    """
    type_requis = None

    def get_entreprise(self):
        return entreprise_de(self.request.user)

    def test_func(self):
        entreprise = self.get_entreprise()
        if entreprise is None:
            return False
        return self.type_requis is None or entreprise.type_entreprise == self.type_requis

    def handle_no_permission(self):
        user = self.request.user
        # un compte qui n'a pas encore cree son entreprise est envoye vers sa creation
        if user.is_authenticated and self.get_entreprise() is None:
            return redirect('entreprises_create')
        return super().handle_no_permission()


class TransporteurRequisMixin(EntrepriseRequiseMixin):
    type_requis = 'transporteur'


class ChargeurRequisMixin(EntrepriseRequiseMixin):
    type_requis = 'chargeur'


class SansEntrepriseRequisMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Creation d'entreprise : utilisateur connecte qui n'en gere pas encore (relation 1-1)."""
    def test_func(self):
        return entreprise_de(self.request.user) is None


class EntrepriseCouranteFormMixin:
    """Fixe form.instance.entreprise cote serveur a partir de request.user, AVANT la validation :
    les regles metier du clean() du modele s'appliquent ainsi au formulaire (erreurs affichees)
    au lieu d'echouer plus tard dans save()."""
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.entreprise = self.get_entreprise()
        return form
