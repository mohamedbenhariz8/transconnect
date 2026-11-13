from django import forms
from .models import Vehicule
from EntreprisesApp.models import Entreprise

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'
        exclude = ['updated_at','created_at','id'] 
        widgets = {'immatriculation': forms.TextInput(attrs={'placeholder': '123 TU 4567'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entreprise'].queryset = Entreprise.objects.filter(type_entreprise='transporteur')
