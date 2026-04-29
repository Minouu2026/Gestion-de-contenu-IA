from extensions import db
from datetime import datetime, timezone

class Interaction(db.Model):
    __tablename__ = "interactions"
    
    #colonnes
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    visiteur_id = db.Column(db.String(100), nullable=False)
    type_action = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<Interaction visiteur={self.visiteur_id} | article={self.article_id} | action={self.type_action}>"
    