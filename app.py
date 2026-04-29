from flask import Flask, render_template, request, jsonify, redirect, url_for
from extensions import db
from dotenv import load_dotenv
from config import Config
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

#import les modèles
from models.article import Article
from models.interaction import Interaction

#import des services IA
from services.analyse import get_articles_populaires, get_articles_faibles
from services.suggestion import get_suggestions

#routes pour le visiteur
@app.route("/")
def index():
    """Page d'accueil - affiche les aricles + suggestions IA."""
    articles = Article.query.all()
    suggestions = get_suggestions()
    return render_template("index.html", articles=articles, suggestions=suggestions)

@app.route("/article/<int:id>")
def article_detail(id):
    """Fiche article - enregistre une automatiquement."""
    article = Article.query.get_or_404(id)
    #enregistre la vue
    article.vues += 1
    
    interaction = Interaction(
        article_id=article.id,
        visiteur_id=request.remote_addr,
        type_action="vue"
    )
    db.session.add(interaction)
    db.session.commit()
    from services.suggestion import get_suggestions_par_categorie 
    similaires = get_suggestions_par_categorie(article.categorie)
    similaires = [a for a in similaires if a.id != article.id]
    return render_template("article_detail.html", article=article, similaires=similaires)

@app.route("/like/<int:id>", methods=["POST"])
def like_article(id):
    """Like un article."""
    article = Article.query.get_or_404(id)
    article.likes += 1
    interaction = Interaction(
        article_id=article.id,
        visiteur_id=request.remote_addr,
        type_action="like"
    )
    db.session.add(interaction)
    db.session.commit()
    return jsonify({"likes": article.likes})

#routes pour l'admin
@app.route("/dashboard")
def dashboard():
    """Dashboard admin - tableau articles, populaires, faibles."""
    populaires = get_articles_populaires()
    faibles = get_articles_faibles()
    tous = Article.query.all()
    return render_template(
        "dashboard.html",
        populaires=populaires,
        faibles=faibles,
        tous=tous
    )

@app.route("/dashboard/booster/<int:id>", methods=["POST"])
def booster_article(id):
    """Admin booste un article faible - l'IA va le mettre en avant."""
    try:
        article = Article.query.get_or_404(id)
        article.boosted = True
        db.session.commit()
        print(f"article {article.nom} boosté avec suucès")
        return redirect(url_for("dashboard"))
    except Exception as e:
        print(f" ERREUR boost : {e}")
        db.session.rollback()
        return redirect(url_for("dashboard"))
@app.route("/dashboard/ajouter", methods=["GET", "POST"])
def ajouter_article():
    """Admin ajouter un nouvel article."""
    if request.method == "POST":
        article = Article(
            nom=request.form["nom"],
            prix=float(request.form["prix"]),
            categories=request.form["description"],
            image=request.form.get("image", "default.jpg"),
        )
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("ajouter.html")

@app.route("/dashboard/supprimer/<int:id>", methods=["POST"])
def supprimer_article(id):
    """Admin supprime un article."""
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("dashboard"))

#lancement
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
