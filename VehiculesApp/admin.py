from django.contrib import admin
from .models import Vehicule
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
    search_fields = ('immatriculation', 'type_vehicule', 'entreprise__raison_sociale')
    list_filter = ('type_vehicule', 'disponible', 'entreprise')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('immatriculation',)
    list_editable = ( 'disponible',)
    list_per_page = 10
    fieldsets = (
        ('Identification du Véhicule', {
            'fields': ('immatriculation', 'type_vehicule', 'entreprise')
        }),
        ('Capacité & Disponibilité', {
            'fields': ('capacite_kg', 'disponible')
        }),
        ('Dates & Traçabilité', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
# Register your models here.
admin.site.register(Vehicule, VehiculeAdmin)