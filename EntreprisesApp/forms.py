from django import forms
from .models import Entreprise, utilisateur

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = '__all__'
        exclude = ['updated_at','created_at','id']  
        widgets = {'matricule_fiscal': forms.TextInput(attrs={'placeholder': '1234567/A/B/C/123'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gerant'].queryset = utilisateur.objects.filter(entreprise__isnull=True) | utilisateur.objects.filter(pk=self.instance.gerant_id)
