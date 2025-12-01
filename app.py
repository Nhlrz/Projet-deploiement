from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import json
import secrets
import bcrypt

app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("API_SECRET_KEY", secrets.token_hex(16))

with open("users.json") as f:
    USERS = json.load(f)

SESSIONS = {}


def validate_credentials(username, password):
    hashed = USERS.get(username)
    if not hashed:
        return False
    return bcrypt.checkpw(password.encode(), hashed.encode())

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    username = data["username"]
    password = data["password"]

    if validate_credentials(username, password):
        token = secrets.token_hex(32)
        SESSIONS[token] = username
        return jsonify({"status": "success", "token": token}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid username or password"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"status": "error", "message": "Invalid token"}), 401
    token = auth.split()[1]
    SESSIONS.pop(token, None)
    return jsonify({"status": "success", "message": "Logged out"}), 200

#middleware
@app.before_request
def check_token():
    public_endpoints = {"login", "get_recap_values", "static"}
    if request.endpoint in public_endpoints or request.method == "OPTIONS":
        return

    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"status": "unauthorized", "message": "Missing token"}), 401

    token = auth.split()[1]
    if token not in SESSIONS:
        return jsonify({"status": "unauthorized", "message": "Invalid token"}), 401

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to insert data
        query = "INSERT INTO {} (hostname, ip, sgbd) VALUES (%s, %s, %s)".format(data['db_table'])
        values = (data['server_name'], data['server_ip'], data['sgbd_type'])
        cursor.execute(query, values)
        conn.commit()

        return jsonify({"message": "Data inserted successfully", "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/get_info_version', methods=['POST'])
def get_info_version():
    try:
        data = request.get_json()
        if not data or 'db_table' not in data or 'version' not in data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL query to select data
        #query = "SELECT CASE WHEN EXISTS(SELECT 1 FROM {} WHERE version = %s) THEN 1  ELSE 0  END AS version".format(data['db_table'])
        query = "SELECT COALESCE((SELECT id_ref_softwares FROM ref_softwares WHERE version = %s ), 0 ) AS version".format(data['db_table'])
        cursor.execute(query, (data['version'],))
        result = cursor.fetchall()

        return jsonify({"data": result, "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/get_info_server', methods=['POST'])
def get_info_server():
    try:
        data = request.get_json()
        if not data or 'db_table' not in data or 'server_name' not in data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL query to select data
        query = "SELECT COALESCE((SELECT id_ref_servers FROM {} WHERE server_name = %s ), 0 ) AS id_ref_servers".format(data['db_table'])
        cursor.execute(query, (data['server_name'],))
        result = cursor.fetchall()

        return jsonify({"data": result, "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/set_info_version', methods=['POST'])
def set_info_version():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL query to insert data
        query = "INSERT INTO {} (software, version) VALUES (%s, %s)".format(data['db_table'])
        values = (data['software'], data['version'])
        cursor.execute(query, values)
        #result = cursor.fetchall()

        # Récupérer l'ID de la dernière insertion
        last_id = cursor.lastrowid

        conn.commit()

        #return jsonify({"data": result, "status": "success"}), 200
        #return jsonify({"data": last_id, "status": "success"}), 200
        return jsonify({"data": {"last_insert_id": last_id}, "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/set_info_server', methods=['POST'])
def set_info_server():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL query to insert data
        query = "INSERT INTO {} (server_name,ip,id_ref_env,id_ref_softwares) VALUES (%s, %s, %s,%s)".format(data['db_table'])
        values = (data['server_name'], data['server_ip'], data['server_env'], data['id_software'])
        cursor.execute(query, values)
        #result = cursor.fetchall()

        # Récupérer l'ID de la dernière insertion
        last_id = cursor.lastrowid

        conn.commit()

        #return jsonify({"data": result, "status": "success"}), 200
        return jsonify({"data": {"last_insert_id": last_id}, "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/delete', methods=['DELETE'])
def delete_data():
    try:
        data = request.get_json()
        if not data or 'server_ip' not in data:
            return jsonify({"message": "Invalid input, 'server_ip' is required", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to delete data based on IP address
        query = "DELETE FROM {} WHERE ip = %s".format(data['db_table'])
        values = (data['server_ip'],)
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No matching record found for the provided IP", "status": "error"}), 404

        return jsonify({"message": "Data deleted successfully", "status": "success"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/set_db_server', methods=['POST'])
def set_db_server():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        # Sécurisation du nom de la table
        db_table = data['db_table'].replace("`", "")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Vérifier si la donnée existe déjà
        check_query = f"SELECT id_ref_databases FROM `{db_table}` WHERE id_ref_servers = %s AND database_name = %s"
        cursor.execute(check_query, (data['id_ref_server'], data['db_name']))
        existing_entry = cursor.fetchone()

        if existing_entry:
            return jsonify({
                "message": "Entry already exists",
                "existing_id": existing_entry["id_ref_databases"],
                "status": "exists"
            }), 200

        # Insérer la nouvelle donnée si elle n'existe pas
        insert_query = f"INSERT INTO `{db_table}` (id_ref_servers, database_name) VALUES (%s, %s)"
        cursor.execute(insert_query, (data['id_ref_server'], data['db_name']))

        last_id = cursor.lastrowid
        conn.commit()

        return jsonify({"data": {"last_insert_id": last_id}, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/set_user_db', methods=['POST'])
def set_user_db():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        # Sécurisation du nom de la table
        db_table = data['db_table'].replace("`", "")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Vérifier si la donnée existe déjà
        #check_query = f"SELECT id_ref_databases FROM `{db_table}` WHERE id_ref_servers = %s AND database_name = %s"
        check_query = f"SELECT id_ref_users FROM `{db_table}` WHERE id_ref_servers = %s AND User = %s AND Host = %s "
        cursor.execute(check_query, (data['id_ref_servers'], data['dbuser'], data['dbhost']))
        existing_entry = cursor.fetchone()

        if existing_entry:
            return jsonify({
                "message": "Entry already exists",
                "existing_id": existing_entry["id_ref_users"],
                "status": "exists"
            }), 200

        # Insérer la nouvelle donnée si elle n'existe pas
        insert_query = f"INSERT INTO `{db_table}` (id_ref_servers, User, Host) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (data['id_ref_servers'], data['dbuser'], data['dbhost']))

        last_id = cursor.lastrowid
        conn.commit()

        return jsonify({"data": {"last_insert_id": last_id}, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/insert_server_recap', methods=['POST'])
def insert_server_recap():
    try:
        data = request.get_json()
        if not data or 'server_name' not in data:
            return jsonify({"message": "Invalid input, 'server_name' is required", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Vérifier si le serveur existe déjà
        check_query = "SELECT id_ref_recap FROM ref_recap WHERE server_name = %s"
        cursor.execute(check_query, (data['server_name'],))
        existing_entry = cursor.fetchone()

        if existing_entry:
            return jsonify({
                "message": "Server already exists in ref_recap",
                "existing_id": existing_entry[0],
                "status": "exists"
            }), 409

        # Insérer le server_name dans ref_recap
        insert_query = "INSERT INTO ref_recap (server_name) VALUES (%s)"
        cursor.execute(insert_query, (data['server_name'],))
        last_id = cursor.lastrowid
        conn.commit()

        return jsonify({"data": {"last_insert_id": last_id}, "status": "success"}), 200
    
    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
@app.route('/insert_recap_values', methods=['POST'])
def insert_recap_values():
    try:
        data = request.get_json()
        if not data or 'server_name' not in data or 'value_data' not in data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Vérifier si le serveur existe déjà dans ref_recap
        check_query = "SELECT id_ref_recap FROM ref_recap WHERE server_name = %s"
        cursor.execute(check_query, (data['server_name'],))
        existing_entry = cursor.fetchone()

        if not existing_entry:
            return jsonify({
                "message": "Server not found in ref_recap",
                "status": "error"
            }), 404

        id_ref_recap = existing_entry['id_ref_recap']

        # Insérer les valeurs dans lnk_recap_values
        insert_query = f"INSERT INTO lnk_recap_values (id_ref_recap, value_name, value_data) VALUES (%s, %s, %s)"

        for key, value in data['value_data'].items():
            cursor.execute(insert_query, (id_ref_recap, key, value))

        conn.commit()

        return jsonify({"message": "Recap values inserted successfully", "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/feed_dbai', methods=['POST'])
def feed_dbai():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Add date to the scan
        from datetime import datetime
        insert_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update query to accept 11 parameters
        check_query = f"SELECT feed_dbai(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(check_query, (data['server'], data['ip_address'], data['cluster_name'], data['env'], data['site'], data['project'], data['db_engine'], data['db_engine_version'], data['databases'], data['users'], insert_date))
        new_id = cursor.fetchone()

        conn.commit()

        return jsonify({"data": {"new_id": new_id}, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/mysql_sniffer', methods=['POST'])
def mysql_sniffer():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Insère dans DBAI
        check_query = f"SELECT mysql_sniffer(%s, %s, %s, %s, %s, %s)"
        cursor.execute(check_query, (data['server'], data['ip_address'], data['site'], data['runner'], data['dbms_type'], data['dbms_status']))
        new_id = cursor.fetchone()

        conn.commit()

        return jsonify({"data": {"new_id": new_id}, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/mysql_sniffer_hosts', methods=['POST'])
def mysql_sniffer_hosts():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Invalid input", "status": "error"}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Appelle la procédure stockée
        cursor.callproc("mysql_sniffer_servers", (data['site'], data['dbms_type'], data['dbms_status']))

        results = []
        # Récupère le résultat du SELECT dans la procédure
        for result in cursor.stored_results():
            results.extend(result.fetchall())

        return jsonify({"data": results, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/get_recap_values', methods=['GET'])
def get_recap_values():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL query to fetch all recap values
        query = """
        SELECT lrv.value_name, lrv.value_data, lrv.date, rr.server_name
        FROM lnk_recap_values lrv
        JOIN ref_recap rr ON lrv.id_ref_recap = rr.id_ref_recap
        """
        cursor.execute(query)
        result = cursor.fetchall()

        return jsonify({"data": result, "status": "success"}), 200

    except mysql.connector.Error as err:
        return jsonify({"message": str(err), "status": "error"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    # Check if certificate files exist, if not generate them automatically
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        print("SSL certificate files not found! Generating them automatically...")
        
        try:
            import subprocess
            import socket
            
            # Get server hostname for the certificate
            hostname = socket.gethostname()
            
            # Generate self-signed certificate with server hostname
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', 
                '-nodes', '-out', 'cert.pem', '-keyout', 'key.pem', 
                '-days', '365', '-subj', f'/CN={hostname}'
            ], check=True)
            
            print(f"SSL certificates generated successfully for hostname: {hostname}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error generating SSL certificates: {e}")
            print("Falling back to manual certificate generation instructions...")
        except FileNotFoundError:
            print("OpenSSL not found! Please install OpenSSL or generate certificates manually:")
    
    # Create SSL context and start server
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    print("Starting HTTPS server on port 443...")
    app.run(host='0.0.0.0', port=443, debug=False, threaded=True, ssl_context=context)