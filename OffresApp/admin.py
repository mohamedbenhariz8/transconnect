from django.contrib import admin

from .models import offre
class offreAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'expedition', 'vehicule')
    search_fields = ('entreprise__raison_sociale', 'expedition__reference', 'vehicule__immatriculation')
    list_filter = ('entreprise', 'expedition' )
    list_display_links = ('expedition',)
    list_editable = ('entreprise',)
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')
    fieldsets = (
        ('Détails de l\'Expédition & Transporteur', {
            'fields': ('expedition', 'entreprise', 'vehicule')
        }),
        ('Offre Commerciale', {
            'fields': ('prix', 'delai_jours', 'statut')
        }),
        ('Dates & Traçabilité', {
            'classes': ('collapse',),
            'fields': ('date_proposition', 'created_at', 'updated_at')
        }),
    )

# Register your models here.
admin.site.register(offre, offreAdmin)