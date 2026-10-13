from django.contrib import admin
from .models import Entreprise, utilisateur
# Register your models here.

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'type_entreprise', 'adresse','gerant')
    list_editable = ('type_entreprise', 'adresse','gerant')
    search_fields = ('raison_sociale', 'matricule_fiscal', 'adresse','gerant')
    list_filter = ('type_entreprise', 'gerant')
    ordering = ('raison_sociale',)
    list_per_page = 5
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Entreprise,EntrepriseAdmin)
admin.site.register(utilisateur)