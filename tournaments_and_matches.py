from database.tournaments_queries import add_tournament, get_tournament_by_id, update_tournament_score
from database.history_queries import add_history


def create_new_tournament(
        club_id,
        club_position,
        opponent_club_ids,
        opponent_forces,
        positions,
        round,
        status,
        start_date,
        score):
    """Créer un tournoi dans la base de données"""
    add_tournament(
        club_id,
        club_position,
        *opponent_club_ids,
        *opponent_forces,
        *positions,
        round,
        status,
        start_date,
        None,
        score)

    # Ajouter un historique pour l'action
    action_details = f"Tournoi créé avec {club_id} en position {club_position} contre {
        ', '.join(
            map(
                str,
                opponent_club_ids))}."
    add_history("tournament", club_id, "création", action_details)


def update_match_score(tournament_id, score):
    """Mettre à jour le score d'un tournoi"""
    tournament = get_tournament_by_id(tournament_id)
    if tournament:
        update_tournament_score(tournament_id, score)
        # Ajouter un historique pour la mise à jour du score
        action_details = f"Score du tournoi {tournament_id} mis à jour à {score}."
        add_history("tournament", tournament_id, "score", action_details)
