from app import app 
from extensions import db
from models.article import Article

with app.app_context():
   db.create_all()
   if Article.query.count() == 0:
    articles = [
        Article(nom="Robe élégante", prix=45000, categorie="Robe", description="Robe longue noir", image="robeElegante.jpg"),
        Article(nom="Sac cuir", prix=90000, categorie="Sac", description="sac en cuir marron", image="sacCuir.jpg"),
        Article(nom="Chaussure talon", prix=78000, categorie="Chaussure", description="Talons dorés", image="talon.jpg"),
        Article(nom="Jupe crayon", prix=25000, categorie="Jupe", description="Jupe crayon class et moderne", image="jupeCrayon.jpg"),
        Article(nom="Lunette de soleil", prix=12000, categorie="Lunette", description="Lunette qui vous vas quelque soit votre style", image="lunette.jpg"),
    
    ]
    db.session.add_all(articles)
    db.session.commit()
    print("Article ajoutés !")

