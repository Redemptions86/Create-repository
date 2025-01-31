# utils/format_table.py

from functools import wraps
from tabulate import tabulate

def format_as_table(headers):
    """
    Décorateur pour formater automatiquement les résultats d'une commande en tableau.
    Args:
        headers (list): Liste des en-têtes de colonnes.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            try:
                # Exécuter la fonction de commande
                rows = await func(ctx, *args, **kwargs)
                if rows:
                    # Utiliser tabulate pour formater les données en tableau
                    table = tabulate(rows, headers=headers, tablefmt="pretty")
                    await ctx.send(f"```{table}```")  # Afficher le tableau dans Discord
                else:
                    await ctx.send("Aucune donnée trouvée.")
            except Exception as e:
                # Gérer les erreurs en utilisant ctx.send
                if hasattr(ctx, "send"):
                    await ctx.send(f"Erreur : {e}")
                else:
                    raise e  # Renvoyer l'exception si `ctx.send` n'est pas disponible
        return wrapper
    return decorator
