from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from .models import expedition
from OffresApp.models import offre

class OffreInline(admin.TabularInline):
    model = offre
    extra = 0
    fk_name = 'expedition'
    fields = ('entreprise', 'vehicule', 'prix', 'delai_jours', 'statut')
    readonly_fields = ('entreprise', 'vehicule', 'prix', 'delai_jours', 'statut')
    show_change_link = True
    can_delete = False

class en_retard(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        if self.value() == "oui":
            return queryset.filter(statut="publiee", date_souhaitee__lt=timezone.now().date())
        elif self.value() == "non":
            return queryset.exclude(statut="publiee", date_souhaitee__lt=timezone.now().date())
        return queryset

class expeditionAdmin(admin.ModelAdmin):
    inlines = [OffreInline]
    list_display = ('reference', 'date_souhaitee', 'ville_depart', 'ville_arrivee', 'poids_kg', 'statut_colore', 'entreprise')
    list_filter = ('statut', 'date_souhaitee', 'entreprise', en_retard)
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_sociale')
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaitee'
    readonly_fields = ('reference', 'created_at', 'updated_at', 'statut_colore')
    list_per_page = 25
    actions = [
        'cloturer_expeditions',
        'marquer_comme_publiee',
        'marquer_comme_attribuee',
        'marquer_comme_en_cours',
        'marquer_comme_terminee',
    ]
    fieldsets = (
        (None, {
            'fields': ('reference', 'entreprise', 'statut', 'statut_colore')
        }),
        ('Trajet', {
            'fields': ('ville_depart', 'ville_arrivee', 'date_souhaitee')
        }),
        ('Marchandise', {
            'fields': ('poids_kg', 'description')
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'publiee': '#F0AD4E',
            'attribuee': '#17A2B8',
            'en cours': '#007BFF',
            'terminee': '#28A745',
        }
        couleur = couleurs.get(obj.statut, '#6c757d')
        return format_html(
            '<span style="color:white; background-color:{}; padding:3px 10px; border-radius:4px; font-weight:bold;">{}</span>',
            couleur,
            obj.get_statut_display(),
        )

    @admin.action(description="Clôturer les expéditions sélectionnées")
    def cloturer_expeditions(self, request, queryset):
        expeditions_en_cours = queryset.filter(statut='en cours')
        nb_cloturees = 0
        for exp in expeditions_en_cours:
            exp.statut = 'terminee'
            exp.full_clean()
            exp.save()
            nb_cloturees += 1

        if nb_cloturees > 0:
            self.message_user(
                request,
                f"{nb_cloturees} expédition(s) en cours ont été clôturée(s) avec succès.",
                messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "Aucune expédition sélectionnée n'était au statut 'en cours'.",
                messages.WARNING,
            )

    @admin.action(description="Marquer la sélection comme : Publiée")
    def marquer_comme_publiee(self, request, queryset):
        updated = queryset.update(statut='publiee', updated_at=timezone.now())
        self.message_user(request, f"{updated} expédition(s) marquée(s) comme Publiée.", messages.SUCCESS)

    @admin.action(description="Marquer la sélection comme : Attribuée")
    def marquer_comme_attribuee(self, request, queryset):
        updated = queryset.update(statut='attribuee', updated_at=timezone.now())
        self.message_user(request, f"{updated} expédition(s) marquée(s) comme Attribuée.", messages.SUCCESS)

    @admin.action(description="Marquer la sélection comme : En cours")
    def marquer_comme_en_cours(self, request, queryset):
        updated = queryset.update(statut='en cours', updated_at=timezone.now())
        self.message_user(request, f"{updated} expédition(s) marquée(s) comme En cours.", messages.SUCCESS)

    @admin.action(description="Marquer la sélection comme : Terminée")
    def marquer_comme_terminee(self, request, queryset):
        updated = queryset.update(statut='terminee', updated_at=timezone.now())
        self.message_user(request, f"{updated} expédition(s) marquée(s) comme Terminée.", messages.SUCCESS)

# Register your models here.
admin.site.register(expedition, expeditionAdmin)
