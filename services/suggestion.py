from models.article import Article
from models.interaction import Interaction

#Poids IA : un like vaut plus qu'une vue car c'est une action volontaire
POIDS_LIKE = 3
POIDS_VUE = 1

def calculer_score(article):
    """Calcule un score IA pour chaque article. Les articles boostés reçoivent un bonus pour apparître en priorité."""
    score = (article.likes * POIDS_LIKE) + (article.vues * POIDS_VUE)
    
    #bonus boost - l'admin a demandé à mettre cet article en avant
    if article.boosted:
        score += 1000 #Priorité absolue dans les suggestions
    return score

def get_suggestions(limite=6):
    """
    Retourne les articles suggérés aux visiteurs.
    Logique IA :
    1. Les articles boostés par l'admin apparaissent en premier
    2. Ensuite les articles avec le meilleur score (likes + vues)
    """
    
    tous = Article.query.all()
    if not tous:
        return []
    
    #calcule le score de chaque article et trie
    articles_scores = sorted(
        tous, 
        key=lambda a: calculer_score(a),
        reverse=True
    )
    return articles_scores[:limite]

def get_suggestions_par_categorie(categorie, limite=4):
    """Suggestions filtrées par caégorie. Utile sur la fiche article pour suggérer des articles similaires."""
    articles = Article.query.filter_by(categorie=categorie).all()
    if not articles:
        return []
    articles_scores = sorted(
        articles,
        key=lambda a: calculer_score(a),
        reverse=True
    )
    return articles_scores[:limite]

def get_suggestions_visiteur(visiteur_id, limite=6):
    """Suggestions personnalisées basées sur l'historique du visiteur. Regarde les catégories que le visiteur a le plus consultées et suggère les meilleurs articles de ces catégories."""
    #récupère toutes les intéractions du visiteur
    interactions = Interaction.query.filter_by(visiteur_id=visiteur_id).all()
    if not interactions:
        #visiteur inconnu -  retourne les suggestions générales
        return get_suggestions(limite)
    #compte les catégories visitées
    categories_vues = {}
    for interaction in interactions:
        article = Article.query.get(interactions.article_id)
        if article:
            cat = article.categorie
            categories_vues[cat] = categories_vues.get(cat, 0) + 1
    #catégorie favorite du visiteur
    categorie_favorite = max(categories_vues, key=categories_vues.get)
    #suggestions bsées sur la catégorie favorite
    suggestions = get_suggestions_par_categorie(categorie_favorite, limite)
    
    #complète avec des suggestions générales si pas ssez d'articles
    if len(suggestions) < limite:
        generales = get_suggestions(limite)
        for article in generales:
            if article not in suggestions:
                suggestions.append(article)
            if len(suggestions) > limite:
                break
    return suggestions[:limite]
    