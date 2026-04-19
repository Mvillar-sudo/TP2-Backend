from repositories.ranking_repository import get_ranking_from_db, get_total_users

def get_ranking_service(limit, offset):
    """
    Coordina la obtención de datos del repositorio.
    """
    ranking_data = get_ranking_from_db(limit, offset)
    total_users = get_total_users()
    
    return ranking_data, total_users
