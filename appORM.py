import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# --------------------------------------------------
# Configuration Flask & Base de données
# --------------------------------------------------
app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "app")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass123")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# Modèles ORM
# --------------------------------------------------
class Utilisateur(db.Model):
    __tablename__ = "utilisateurs"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(150), nullable=False)
    langue = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "mail": self.mail,
            "langue": self.langue,
        }


class Film(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    duree = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "annee": self.annee,
            "duree": self.duree,
        }
class Director(db.Model):
    __tablename__ = "directors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    films = db.relationship(
        "Film",
        back_populates="director",
        cascade="all, delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

# --------------------------------------------------
# Routes Utilisateurs
# --------------------------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    users = Utilisateur.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data.get("username") or not data.get("mail"):
        return jsonify({"error": "username et mail obligatoires"}), 400

    user = Utilisateur(
        username=data["username"],
        mail=data["mail"],
        langue=data.get("langue"),
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur ajouté"}), 201


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Utilisateur.query.get(user_id)

    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur supprimé"}), 200

# --------------------------------------------------
# Routes Films
# --------------------------------------------------
@app.route("/films", methods=["GET"])
def get_films():
    films = Film.query.all()
    return jsonify([f.to_dict() for f in films])


@app.route("/films", methods=["POST"])
def create_film():
    data = request.get_json()

    if not data.get("titre") or not data.get("annee") or not data.get("duree"):
        return jsonify({"error": "titre, annee et duree obligatoires"}), 400

    film = Film(
        titre=data["titre"],
        annee=data["annee"],
        duree=data["duree"],
    )

    db.session.add(film)
    db.session.commit()

    return jsonify({"message": "Film ajouté"}), 201


@app.route("/films/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    film = Film.query.get(film_id)

    if not film:
        return jsonify({"error": "Film introuvable"}), 404

    db.session.delete(film)
    db.session.commit()

    return jsonify({"message": "Film supprimé"}), 200

# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    print("🚀 API Flask lancée sur http://127.0.0.1:5000")
    app.run(debug=True)
