from django.contrib import admin

from .models import expedition
class expeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'date_souhaitee', 'ville_depart', 'ville_arrivee', 'poids_kg', 'statut', 'entreprise')
    list_filter = ('statut', 'date_souhaitee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_sociale')
    ordering = ('date_souhaitee',)
    list_editable = ('statut',)
    readonly_fields = ('reference', 'created_at', 'updated_at')
    list_per_page = 10
    fieldsets = (
        (None,
        {'fields': ('reference', 'entreprise', 'statut')}),
        ('Trajet', {'fields': ('ville_depart', 'ville_arrivee', 'date_souhaitee')}),
        ('Marchandise', {'fields': ('poids_kg', 'description')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

# Register your models here.
admin.site.register(expedition, expeditionAdmin)
