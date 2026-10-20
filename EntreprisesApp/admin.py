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

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_staff')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    list_filter = ('role', 'is_staff', 'is_active')
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Identifiants & Profil', {
            'fields': ('user_id', 'username', 'email', 'telephone', 'role')
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

admin.site.register(Entreprise, EntrepriseAdmin)
admin.site.register(utilisateur, UtilisateurAdmin)