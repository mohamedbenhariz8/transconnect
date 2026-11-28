from django import forms
from .models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        # entreprise : fixee cote serveur a partir de request.user
        fields = ['immatriculation', 'type_vehicule', 'capacite_kg', 'disponible']
        widgets = {'immatriculation': forms.TextInput(attrs={'placeholder': '123 TU 4567'})}
