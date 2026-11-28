from django import forms
from .models import offre
from ExpeditionsApp.models import expedition
from VehiculesApp.models import Vehicule

class OffreForm(forms.ModelForm):
    class Meta:
        model = offre
        # entreprise : fixee cote serveur ; statut : change uniquement par le chargeur (accepter / refuser)
        fields = ['expedition', 'vehicule', 'prix', 'delai_jours']
        widgets = {'prix': forms.NumberInput(attrs={'placeholder': 'prix en DT'})}

    def __init__(self, *args, entreprise=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expedition'].queryset = expedition.objects.filter(statut='publiee') | expedition.objects.filter(pk=self.instance.expedition_id)
        # uniquement les vehicules disponibles du transporteur connecte
        self.fields['vehicule'].queryset = Vehicule.objects.filter(entreprise=entreprise, disponible=True) | Vehicule.objects.filter(pk=self.instance.vehicule_id)
