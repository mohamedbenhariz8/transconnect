from django.db import models
from EntreprisesApp.models import Entreprise
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.
class expedition(models.Model):
    reference=models.CharField(max_length=20,unique=True)
    ville_depart=models.CharField(max_length=100)
    ville_arrivee=models.CharField(max_length=100)
    poids_kg=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01,"poids doit etre superieur a 0")])
    date_souhaitee=models.DateField()
    description=models.TextField()
    statut=models.CharField(max_length=20,choices=[ ('publiee','Publiee'), ('attribuee','Attribuee'), ('en cours','En Cours'), ('terminee','Terminee') ],default='publiee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='expeditions')
    def clean(self):
        super().clean()
        
        if self.entreprise_id and self.entreprise.type_entreprise != 'chargeur':
            raise ValidationError({'entreprise': "une expedition ne peut etre cree que par une entreprise de type chargeur"})
    @classmethod
    def _generate_ref(cls):
        annee = timezone.now().strftime('%y')

        prefix = f"EXP_{annee}_"
        dernier = cls.objects.filter(reference__startswith=prefix).order_by('-reference').first()
        compteur= int(dernier.reference[-5:])+1 if dernier else 1
        
        if compteur>99999:
            raise ValidationError("Le compteur de référence a dépassé la limite de 99999.")

        return f"{prefix}{compteur:05d}"        
    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_ref()
        self.full_clean() 
        super().save(*args, **kwargs)