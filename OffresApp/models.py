from django.db import models
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import expedition
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