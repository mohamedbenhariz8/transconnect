from django.db import models
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import expedition
from django.core.exceptions import ValidationError
# Create your models here.
class offre (models.Model):
    prix=models.DecimalField(max_digits=10, decimal_places=2)
    delai_jours=models.IntegerField()   
    status=models.CharField(max_length=20,choices=[ ('refuse','Refuse'), ('accepte','Accepte'), ('en cours','En Cours') ],default='en cours')
    date_proposition=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='offres')
    expedition=models.ForeignKey(expedition,on_delete=models.CASCADE,related_name='offres')

    # Vehicules
    def clean(self):
        super().clean()
        #regle(s) metier
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "une offre ne peut etre faite que par une entreprise de type transporteur"})
