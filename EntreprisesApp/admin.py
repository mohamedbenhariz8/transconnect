from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from VehiculesApp.models import Vehicule
from .models import Entreprise, utilisateur
# Register your models here.
admin.site.site_header = "TransConnect Operations"
admin.site.site_title = "TransConnect Admin"
admin.site.index_title = "Tableau de Bord & Gestion Opérationnelle"
class vehiculeInline(admin.TabularInline): 
    model=Vehicule
    fields=('immatriculation','type_vehicule','capacite_kg','disponible')
    extra = 0   
    show_change_link=True

class EntrepriseAdmin(admin.ModelAdmin):
    inlines=[vehiculeInline]
    list_display = ('raison_sociale', 'type_entreprise', 'adresse','gerant')
    list_editable = ('type_entreprise', 'adresse','gerant')
    search_fields = ('raison_sociale', 'matricule_fiscal', 'adresse','gerant')
    list_filter = ('type_entreprise', 'gerant')
    ordering = ('raison_sociale',)
    list_per_page = 5
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('raison_sociale', 'type_entreprise', 'gerant')
        }),
        ('Coordonnées & Fiscalité', {
            'fields': ('matricule_fiscal', 'adresse')
        }),
        ('Dates & Traçabilité', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = utilisateur
        fields = ('username', 'email', 'telephone', 'role')

class UtilisateurAdmin(UserAdmin):
    add_form = UtilisateurCreationForm
    list_display = ('user_id', 'username', 'email', 'role', 'telephone')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    list_filter = ('role', 'is_staff', 'is_active')
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    ordering = ('user_id',)
    list_per_page = 10
    fieldsets = (
        ('Identifiants & Profil', {
            'fields': ('user_id', 'username', 'password', 'email', 'telephone', 'role')
        }),
        ('Permissions & Accès', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )
    add_fieldsets = (
        ('Création de l\'Utilisateur', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telephone', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(Entreprise, EntrepriseAdmin)
admin.site.register(utilisateur, UtilisateurAdmin)