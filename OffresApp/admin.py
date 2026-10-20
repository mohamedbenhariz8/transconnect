import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import offre

@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="offres.csv"'
    writer = csv.writer(response)
    writer.writerow(['reference_expedition', 'transporteur', 'prix', 'statut'])
    for obj in queryset.select_related('expedition', 'entreprise'):
        writer.writerow([
            obj.expedition.reference,
            obj.entreprise.raison_sociale,
            obj.prix,
            obj.statut,
        ])
    return response

class offreAdmin(admin.ModelAdmin):
    list_display = ('expedition', 'entreprise', 'vehicule', 'prix', 'delai_jours', 'statut_colore')
    list_filter = ('statut', 'entreprise', 'expedition')
    search_fields = ('entreprise__raison_sociale', 'expedition__reference', 'vehicule__immatriculation')
    list_display_links = ('expedition',)
    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 10
    actions = [exporter_offres_csv]
    autocomplete_fields = ('expedition', 'entreprise', 'vehicule')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at', 'statut_colore')
    
    fieldsets = (
        ('Détails de l\'offre', {
            'fields': ('expedition', 'entreprise', 'vehicule')
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours')
        }),
        ('Suivi', {
            'fields': ('statut_colore', 'date_proposition', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'proposee': '#F0AD4E', 
            'acceptee': '#5CB85C',
            'refusee': '#D9534F', 
            'retiree': '#777777',
        }
        couleur = couleurs.get(obj.statut, '#999999')
        return format_html(
            '<span style="color:white; background-color:{}; padding:3px 8px; border-radius:4px; font-weight:bold;">{}</span>',
            couleur,
            obj.get_statut_display(),
        )

    def get_readonly_fields(self, request, obj=None):
        base = list(self.readonly_fields)
        if obj and obj.statut == 'acceptee':
            return base + ['prix', 'delai_jours']
        return base

# Register your models here.
admin.site.register(offre, offreAdmin)
