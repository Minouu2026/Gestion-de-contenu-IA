from app import app 
from extensions import db
from models.article import Article

with app.app_context():
    Article.query.delete()
    db.session.commit()
    articles = [
        Article(nom="Robe élégante", prix=45000, categorie="Robe", description="Robe longue noir", image="robeElegante.JPG"),
        Article(nom="Sac cuir", prix=90000, categorie="Sac", description="sac en cuir marron", image="sacCuir.JPG"),
        Article(nom="Chaussure talon", prix=78000, categorie="Chaussure", description="Talons dorés", image="talon.JPG"),
        Article(nom="Jupe crayon", prix=25000, categorie="Jupe", description="Jupe crayon class et moderne", image="jupeCrayon.JPG"),
        Article(nom="Lunette de soleil", prix=12000, categorie="Lunette", description="Lunette qui vous vas quelque soit votre style", image="lunette.JPG"),
    
    ]
    db.session.add_all(articles)
    db.session.commit()
    print("Article ajoutés !")
