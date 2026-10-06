from django.db import models
from EntreprisesApp.models import Entreprise
from OffresApp.models import offre
from django.core.validators import MinValueValidator 
# Create your models here.
class vehicule(models.Model):
    immatriculation=models.CharField(max_length=15,unique=True)
    type_vebicule=models.CharField(max_length=20,choices=
    [
    ('camion porteur','Camion Porteur'),
    ('camionette','Camionette'),
    ('semi-remorque','Semi-Remorque'),
    ('fourgon','Fourgon'),
    ],default='camionette')
    
    
    capacite=models.IntegerField(validators=[minValueValidator(100,"capacite doit etre superieur a 100")])
    disponibilite=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='vehicules')
    offre=models.ForeignKey(offre,on_delete=models.CASCADE,related_name='vehicules',null=True,blank=True)