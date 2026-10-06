from django.db import models, transaction
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import expedition
from VehiculesApp.models import Vehicule, CAPACITE_MAX_KG
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
class offre (models.Model):
    prix=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, "Le prix doit être supérieur à 0")])
    delai_jours=models.IntegerField(validators=[MinValueValidator(1, "Le délai doit être au moins de 1 jour")])
    status=models.CharField(max_length=20,choices=[ ('proposee','Proposee'), ('acceptee','Acceptee'), ('refusee','Refusee') ],default='proposee')
    date_proposition=models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entreprise =models.ForeignKey(Entreprise,on_delete=models.CASCADE,related_name='offres')
    expedition=models.ForeignKey(expedition,on_delete=models.CASCADE,related_name='offres')
    vehicule=models.ForeignKey(Vehicule,on_delete=models.CASCADE,related_name='offres')
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'transporteur':
            raise ValidationError({'entreprise': "une offre ne peut etre faite que par une entreprise de type transporteur"})
        if self.vehicule_id and self.vehicule.entreprise_id != self.entreprise_id:
            raise ValidationError({'vehicule': "le vehicule proposé doit appartenir au meme transporteur"})
        if  self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError({'expedition': "une offre ne peut etre faite que pour une expedition de statut publiee"})

        if self.vehicule_id and  self.vehicule.disponibilite==False:
            raise ValidationError({'vehicule': "ce vehicule n'est pas disponible"})
        if self.vehicule_id and self.expedition_id:
            capacite_max = CAPACITE_MAX_KG.get(self.vehicule.type_vehicule)
            if capacite_max is not None and self.expedition.poids_kg > capacite_max:
                raise ValidationError({'vehicule': f"un vehicule de type {self.vehicule.get_type_vehicule_display()} ne supporte pas plus de {capacite_max} kg (expedition : {self.expedition.poids_kg} kg)"})

    def save(self, *args, **kwargs):
        self.full_clean()  
        ancien_status = None
        if self.pk:
            ancien_status = offre.objects.filter(pk=self.pk).values_list('status', flat=True).first()
        with transaction.atomic():
            super().save(*args, **kwargs)