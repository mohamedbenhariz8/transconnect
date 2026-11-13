from django import forms
from .models import offre
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import expedition
from VehiculesApp.models import Vehicule

class OffreForm(forms.ModelForm):
    class Meta:
        model = offre
        fields = '__all__'
        exclude = ['updated_at','created_at','id','date_proposition']
        widgets = {'prix': forms.NumberInput(attrs={'placeholder': 'prix en DT'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entreprise'].queryset = Entreprise.objects.filter(type_entreprise='transporteur')
        self.fields['expedition'].queryset = expedition.objects.filter(statut='publiee') | expedition.objects.filter(pk=self.instance.expedition_id)
        self.fields['vehicule'].queryset = Vehicule.objects.filter(disponible=True) | Vehicule.objects.filter(pk=self.instance.vehicule_id)
        if not self.instance.pk:
            del self.fields['statut']
