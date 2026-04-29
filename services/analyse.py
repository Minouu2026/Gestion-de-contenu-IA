from models.article import Article

#Seuils IA
SEUIL_POPULAIRE_LIKES = 10
SEUIL_POPULAIRE_VUES = 20
SEUIL_FAIBLE_LIKES = 5
SEUIL_FAIBLE_VUES = 10

def get_articles_populaires():
    """Retourne les articles les plus performants. Triés par likes d'abord, puis par vues."""
    articles = Article.query.filter(
        (Article.likes > SEUIL_POPULAIRE_LIKES) |
        (Article.vues > SEUIL_POPULAIRE_VUES)
    ).order_by(
        Article.likes.desc(),
        Article.vues.desc()
    ).all()
    return articles

def get_articles_faibles():
    """Retourne les articles qui manquent d'interactions. Ce sont les candidats à booster."""
    articles = Article.query.filter(
        Article.likes < SEUIL_FAIBLE_LIKES, 
        Article.vues < SEUIL_FAIBLE_VUES,
        Article.boosted == False #pas déjà boostés
    ).order_by(
        Article.likes.asc(),
        Article.vues.asc()
    ).all()
    return articles

def get_stats_generales():
    """Retourne des statistiques globales pour le dashboard."""
    tous = Article.query.all()
    total_articles = len(tous)
    total_vues = sum(a.vues for a in tous)
    total_likes = sum(a.likes for a in tous)
    total_boostes = sum(1 for a in tous if a.boosted)
    
    #Article le plus aimé
    meilleur = max(tous, key=lambda a: a.likes, default=None)
    return {
        "total_articles" : total_articles,
        "total_vues" : total_vues,
        "total_likes" : total_likes,
        "total_boostes" : total_boostes,
        "meilleur" : meilleur,
    }