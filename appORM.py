import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --------------------------------------------------
# Configuration Flask & Base de données
# --------------------------------------------------
app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

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

    # Relations
    profile = db.relationship("UserProfile", backref="utilisateur", uselist=False, cascade="all, delete-orphan")
    marks = db.relationship("Mark", backref="utilisateur", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "mail": self.mail,
            "langue": self.langue,
        }


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False, unique=True)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Director(db.Model):
    __tablename__ = "director"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    # Relations
    films = db.relationship("Film", backref="director", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
        }


class Film(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    id_director = db.Column(db.Integer, db.ForeignKey("director.id"))

    # Relations
    marks = db.relationship("Mark", backref="film", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "annee": self.annee,
            "duree": self.duree,
            "id_director": self.id_director,
            "director": self.director.to_dict() if self.director else None,
        }


class Mark(db.Model):
    __tablename__ = "mark"

    id = db.Column(db.Integer, primary_key=True)
    id_film = db.Column(db.Integer, db.ForeignKey("film.id"), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)
    mark = db.Column(db.Integer, nullable=False)  # 0-10

    # Unique constraint: one mark per user per film
    __table_args__ = (db.UniqueConstraint("id_film", "id_user", name="unique_user_film_mark"),)

    def to_dict(self):
        return {
            "id": self.id,
            "id_film": self.id_film,
            "id_user": self.id_user,
            "mark": self.mark,
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

    return jsonify({"message": "Utilisateur ajouté", "user": user.to_dict()}), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = Utilisateur.query.get(user_id)

    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    return jsonify(user.to_dict())


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Utilisateur.query.get(user_id)

    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur supprimé"}), 200

# --------------------------------------------------
# Routes UserProfile
# --------------------------------------------------
@app.route("/users/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profil utilisateur introuvable"}), 404

    return jsonify(profile.to_dict())


@app.route("/users/<int:user_id>/profile", methods=["POST"])
def create_user_profile(user_id):
    user = Utilisateur.query.get(user_id)

    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    existing_profile = UserProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return jsonify({"error": "Ce utilisateur a déjà un profil"}), 400

    data = request.get_json()

    profile = UserProfile(
        user_id=user_id,
        bio=data.get("bio"),
        avatar_url=data.get("avatar_url"),
    )

    db.session.add(profile)
    db.session.commit()

    return jsonify({"message": "Profil créé", "profile": profile.to_dict()}), 201


@app.route("/users/<int:user_id>/profile", methods=["PUT"])
def update_user_profile(user_id):
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profil utilisateur introuvable"}), 404

    data = request.get_json()
    profile.bio = data.get("bio", profile.bio)
    profile.avatar_url = data.get("avatar_url", profile.avatar_url)

    db.session.commit()

    return jsonify({"message": "Profil mise à jour", "profile": profile.to_dict()}), 200

# --------------------------------------------------
# Routes Directors
# --------------------------------------------------
@app.route("/directors", methods=["GET"])
def get_directors():
    directors = Director.query.all()
    return jsonify([d.to_dict() for d in directors])


@app.route("/directors", methods=["POST"])
def create_director():
    data = request.get_json()

    if not data.get("name") or not data.get("surname"):
        return jsonify({"error": "name et surname obligatoires"}), 400

    director = Director(
        name=data["name"],
        surname=data["surname"],
    )

    db.session.add(director)
    db.session.commit()

    return jsonify({"message": "Réalisateur ajouté", "director": director.to_dict()}), 201


@app.route("/directors/<int:director_id>", methods=["DELETE"])
def delete_director(director_id):
    director = Director.query.get(director_id)

    if not director:
        return jsonify({"error": "Réalisateur introuvable"}), 404

    db.session.delete(director)
    db.session.commit()

    return jsonify({"message": "Réalisateur supprimé"}), 200

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

    if data.get("id_director"):
        director = Director.query.get(data["id_director"])
        if not director:
            return jsonify({"error": "Réalisateur introuvable"}), 404

    film = Film(
        titre=data["titre"],
        annee=data["annee"],
        duree=data["duree"],
        id_director=data.get("id_director"),
    )

    db.session.add(film)
    db.session.commit()

    return jsonify({"message": "Film ajouté", "film": film.to_dict()}), 201


@app.route("/films/<int:film_id>", methods=["GET"])
def get_film(film_id):
    film = Film.query.get(film_id)

    if not film:
        return jsonify({"error": "Film introuvable"}), 404

    return jsonify(film.to_dict())


@app.route("/films/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    film = Film.query.get(film_id)

    if not film:
        return jsonify({"error": "Film introuvable"}), 404

    db.session.delete(film)
    db.session.commit()

    return jsonify({"message": "Film supprimé"}), 200

# --------------------------------------------------
# Routes Marks (Notes)
# --------------------------------------------------
@app.route("/marks", methods=["GET"])
def get_marks():
    marks = Mark.query.all()
    return jsonify([m.to_dict() for m in marks])


@app.route("/marks", methods=["POST"])
def create_mark():
    data = request.get_json()

    if not data.get("id_film") or not data.get("id_user") or data.get("mark") is None:
        return jsonify({"error": "id_film, id_user et mark obligatoires"}), 400

    if not (0 <= data["mark"] <= 10):
        return jsonify({"error": "mark doit être entre 0 et 10"}), 400

    film = Film.query.get(data["id_film"])
    user = Utilisateur.query.get(data["id_user"])

    if not film:
        return jsonify({"error": "Film introuvable"}), 404
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    existing_mark = Mark.query.filter_by(
        id_film=data["id_film"], id_user=data["id_user"]
    ).first()

    if existing_mark:
        existing_mark.mark = data["mark"]
        db.session.commit()
        return jsonify({"message": "Note mise à jour", "mark": existing_mark.to_dict()}), 200

    mark = Mark(
        id_film=data["id_film"],
        id_user=data["id_user"],
        mark=data["mark"],
    )

    db.session.add(mark)
    db.session.commit()

    return jsonify({"message": "Note ajoutée", "mark": mark.to_dict()}), 201


@app.route("/marks/<int:mark_id>", methods=["DELETE"])
def delete_mark(mark_id):
    mark = Mark.query.get(mark_id)

    if not mark:
        return jsonify({"error": "Note introuvable"}), 404

    db.session.delete(mark)
    db.session.commit()

    return jsonify({"message": "Note supprimée"}), 200


@app.route("/films/<int:film_id>/marks", methods=["GET"])
def get_film_marks(film_id):
    film = Film.query.get(film_id)

    if not film:
        return jsonify({"error": "Film introuvable"}), 404

    marks = Mark.query.filter_by(id_film=film_id).all()
    return jsonify([m.to_dict() for m in marks])

# --------------------------------------------------
# Initialisation de la base de données
# --------------------------------------------------
def init_db():
    """Crée toutes les tables nécessaires dans la base de données"""
    with app.app_context():
        db.create_all()
        print("✅ Tables de la base de données créées avec succès")

# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("🚀 API Flask lancée sur http://127.0.0.1:5000")
    app.run(debug=True)
