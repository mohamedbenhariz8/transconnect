from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.
 
matricule_fiscale=RegexValidator(regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$',
                                 message="Le format du matricule fiscale est invalide. Il doit être au format 1234567/A/B/C/123 ou 1234567-A-B-C-123.")

def validate_email(value):
    if not value :
        raise ValidationError("L'adresse e-mail est obligatoire.")
    if not value.endswith('@gmail.com'):
        raise ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.")


class utilisateur(AbstractUser):
    @classmethod
    def _generate_user_id(cls):
        annee = timezone.now().strftime('%y')  # Obtenir les deux derniers chiffres de l'année
        prefix = f"{annee}user"
        dernier = cls.objects.filter(user_id__startswith=prefix).order_by('-user_id').first()
        compteur = int(dernier.user_id[-2:]) + 1 if dernier else 0
        
        if compteur > 99:
            raise ValidationError("Le compteur d'utilisateur a dépassé la limite de 99 pour cette année.")

        return f"{prefix}{compteur:02d}"
    
    user_id=models.CharField(max_length=8,primary_key=True )
    email = models.EmailField(unique=True,validators=[validate_email])
    
    role=models.CharField(max_length=20,
        choices=[('admin','Admin'),
                 
                 ('user','User')]
        ,default='user')
    telephone=models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200,null=False, blank=False)
    matricule_fiscale = models.CharField(max_length=17,unique=True, validators=[matricule_fiscale])
    type_entreprise = models.CharField(max_length=100,
    choices=[
        ('chargeur','Chargeur'),
        ('transporteur','Transporteur'),
    ],default='chargeur')
    adresse = models.TextField(validators=[MinLengthValidator(20,"adresse doit contenir au moins 20 caracteres"),MaxLengthValidator(300,"adresse doit contenir au plus 300 caracteres")])
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    gerant=models.OneToOneField(utilisateur,on_delete=models.CASCADE,related_name='entreprise',) 
    
    