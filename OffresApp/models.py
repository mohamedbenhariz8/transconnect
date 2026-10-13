from django.db import models, transaction
from EntreprisesApp.models import Entreprise
from ExpeditionsApp.models import expedition
from VehiculesApp.models import Vehicule
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
class offre (models.Model):
    prix=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01, "Le prix doit être supérieur à 0")])
    delai_jours=models.IntegerField(validators=[MinValueValidator(1, "Le délai doit être au moins de 1 jour")])
    statut=models.CharField(max_length=20,choices=[ ('proposee','Proposee'), ('acceptee','Acceptee'), ('refusee','Refusee') ],default='proposee')
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
        if self.vehicule_id and self.transporteur_id and self.vehicule.entreprise_id != self.entreprise_id:
            raise ValidationError({'vehicule': "le vehicule proposé doit appartenir au meme transporteur"})
        if not self.pk and self.expedition_id and self.expedition.statut != 'publiee':
            raise ValidationError({'expedition': "une offre ne peut etre faite que pour une expedition de statut publiee"})
        if self.statut == 'proposee' and self.entreprise_id and self.expedition_id:
            deja = offre.objects.filter(entreprise_id=self.entreprise_id, expedition_id=self.expedition_id, statut='proposee').exclude(pk=self.pk)
            if deja.exists():
                raise ValidationError("cette entreprise a deja une offre proposee sur cette expedition")

        if not self.pk and self.vehicule_id and self.vehicule.disponible==False:
            raise ValidationError({'vehicule': "ce vehicule n'est pas disponible"})
        if self.vehicule_id and self.expedition_id:
            if self.vehicule.type_vehicule == 'camionnette':
                capacite_max = 1500
            elif self.vehicule.type_vehicule == 'fourgon':
                capacite_max = 3500
            elif self.vehicule.type_vehicule == 'camion_porteur':
                capacite_max = 19000
            elif self.vehicule.type_vehicule == 'semi_remorque':
                capacite_max = 26000
            else:
                capacite_max = None
            if capacite_max is not None and self.expedition.poids_kg > capacite_max:
                raise ValidationError({'vehicule': f"un vehicule de type {self.vehicule.get_type_vehicule_display()} ne supporte pas plus de {capacite_max} kg (expedition : {self.expedition.poids_kg} kg)"})

    def save(self, *args, **kwargs):
        self.full_clean()  
        ancien_statut = None
        if self.pk:
            ancien_statut = offre.objects.filter(pk=self.pk).values_list('statut', flat=True).first()
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.statut == 'acceptee' and ancien_statut != 'acceptee':
                expedition.objects.filter(pk=self.expedition_id).update(statut='attribuee')
                offre.objects.filter(expedition_id=self.expedition_id, statut='proposee').exclude(pk=self.pk).update(statut='refusee')