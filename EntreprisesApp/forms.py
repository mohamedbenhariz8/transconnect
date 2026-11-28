from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Entreprise, utilisateur


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        # gerant : jamais choisi par le client (fixe a request.user dans la vue)
        fields = ['raison_sociale', 'matricule_fiscal', 'type_entreprise', 'adresse']
        widgets = {'matricule_fiscal': forms.TextInput(attrs={'placeholder': '1234567/A/B/C/123'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # le type ne change plus apres creation : vehicules, expeditions et offres en dependent
            del self.fields['type_entreprise']


class ProfilForm(forms.ModelForm):
    class Meta:
        model = utilisateur
        # role, is_staff, is_superuser, user_id, mot de passe : jamais modifiables ici
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone']


class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = utilisateur
        # role, is_staff, is_superuser : jamais dans un formulaire d'inscription
        # (un visiteur pourrait se donner lui-meme des droits)
        fields = ('username', 'email', 'telephone')
