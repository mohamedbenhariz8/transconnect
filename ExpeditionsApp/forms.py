from django import forms
from .models import expedition

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = expedition
        # entreprise, reference et statut : jamais fournis par le client
        fields = ['ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'description']
        widgets = {'date_souhaitee': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
