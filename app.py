from flask import Flask, jsonify
from flask import request
import psycopg2

app = Flask(__name__)

# --- Connexion PostgreSQL ---
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="app",
        user="appuser",
        password="pass123"  # modifie ici
    )

# --- Lecture de la table user ---
def fetch_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM utilisateurs;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def fetch_films():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM film;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# --- Affichage au démarrage ---
print("📌 Contenu de la table user :")
try:
    users = fetch_users()
    for u in users:
        print(u)
except Exception as e:
    print("Erreur lors de la lecture de la base :", e)

# --- Route API ---
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = fetch_users()
        # transformation en JSON
        result = [list(row) for row in users]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/films", methods=["GET"])
def get_films():
    try:
        users = fetch_films()
        # transformation en JSON
        result = [list(row) for row in users]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    username = data.get("username")
    mail = data.get("mail")
    langue = data.get("langue")  # peut être None

    if not username or not mail:
        return jsonify({"error": "username et mail sont obligatoires"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO utilisateurs (username, mail, langue) VALUES (%s, %s, %s)",
            (username, mail, langue)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "ok", "message": "Utilisateur ajouté"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/films", methods=["POST"])
def create_film():
    data = request.get_json()

    titre = data.get("titre")
    annee = data.get("annee")
    duree = data.get("duree")  # peut être None

    if not titre or not annee or not duree:
        return jsonify({"error": "titre, duree et annee sont obligatoires"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO film (titre, annee, duree) VALUES (%s, %s, %s)",
            (titre, annee, duree)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "ok", "message": "Film ajouté"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    print("🚀 API Flask lancée sur http://127.0.0.1:5000")
    app.run(debug=True)
