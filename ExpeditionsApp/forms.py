from django import forms
from .models import expedition

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = expedition
        fields = '__all__'       
        exclude = ['reference','updated_at','created_at','id','statut']  # Exclude the 'statut' field from the form
        widgets = {'date_souhaitee': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')} 