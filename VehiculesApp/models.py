from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
CAPACITE_MAX_KG = {
    'camionnette': 1500,
    'fourgon': 3500,
    'camion_porteur': 19000,
    'semi_remorque': 26000,
}
class Vehicule(models.Model):
    immatriculation=models.CharField(max_length=15,unique=True)
    type_vehicule=models.CharField(max_length=20,choices=
    [
    ('camionnette','Camionnette / utilitaire leger'),
    ('camion_porteur','Camion porteur'),
    ('semi_remorque','Semi-remorque'),
    ('fourgon','Fourgon'),
    ],default='camionnette')
    
    
    capacite=models.IntegerField(validators=[MinValueValidator(100,"capacite doit etre superieur a 100")])
    disponibilite=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='vehicules')
    
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
          raise ValidationError({'entreprise': "le vehicule doit appartenir a une entreprise de type transporteur"})