from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.exceptions import ValidationError

# Create your models here.
class expedition(models.Model):
    reference=models.CharField(max_length=20,unique=True)
    ville_depart=models.CharField(max_length=100)
    ville_arrivee=models.CharField(max_length=100)
    poids_kg=models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee=models.DateField()
    description=models.TextField()
    statut=models.CharField(max_length=20,choices=[ ('en attente','En Attente'), ('en cours','En Cours'), ('terminee','Terminee') ],default='en attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='expeditions')
    def clean(self):
        super().clean()
        #regle(s) metier
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "une expedition ne peut etre cree que par une entreprise de type chargeur"})
            