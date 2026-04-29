from extensions import db

class Article(db.Model):
    __tablename__ = "articles"
    
    #colonnes pples
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), default="default.jpg")
    
    #statistiques m à j autom
    vues = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    
    #alert pour l'IA
    boosted = db.Column(db.Boolean, default=False) #si True = l'IA le met en avant
    
    #relation avec les interactions
    interactions = db.relationship("Interaction", backref="article", lazy=True)
    
    def __repr__(self):
        return f"<Article {self.nom} | vues={self.vues} | likes={self.likes} | boosted={self.boosted}>"
    def est_populaire(self):
        """Retourne True si l'article est considéré populaire."""
        return self.likes > 10 or self.vues > 50
    def est_faible(self):
        """Retourne True si l'article manque d'intéractions."""
        return self.likes < 3 and self.vues < 10
    