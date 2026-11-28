from .mixins import entreprise_de


def entreprise_courante(request):
    """Rend {{ mon_entreprise }} disponible dans tous les templates (None si aucune)."""
    return {'mon_entreprise': entreprise_de(request.user)}
