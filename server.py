from flask import Flask, render_template, request, jsonify, Response

import database

from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


# Renvoit l'utilisateur à la page d'accueil de l'application
@app.route("/")
def index():
    return render_template("index.html")


# Retourne toutes les villes desservies par l'agence dans la base de données
# OUTPUT city_names: Liste des villes desservies par l'agence
@app.route("/get_cities", methods=["GET"])
@app.route("/static/client/get_cities", methods=["GET"])
@app.route("/static/admin/get_cities", methods=["GET"])
def get_cities():
    try:
        db = database.Database()
        city_names = db.get_all_ville()

        return jsonify(city_names)
    except Exception as e:
        return Response(status=406)


# Retourne tous les voyages respectant les contraintes sélectionnées par le client lors de la recherche
# INPUT depart: Ville de départ du voyage
# INPUT destination: Ville de destination du voyage
# INPUT date_temps: Date et heure de départ du voyage
# INPUT prix: Tarif du voyage pour un client
# OUTPUT voyages: Liste de voyages respectant les contraintes de recherche
@app.route("/static/client/get_voyages", methods=["POST"])
def get_voyages():
    try:
        db = database.Database()
        data = request.get_json()
        voyages = db.get_voyage(data["depart"], data["destination"], data["date_temps"], data["prix"])
        return jsonify(voyages)
    except Exception as e:
        return Response(status=406)


# Supprime de la base de données un voyage de la liste des voyages du client
# INPUT id_utilisateur: ID du client
# INPUT vo_ni: ID du voyage
# OUTPUT status: Statut de succès de la requête
@app.route("/static/client/delete-voyage/<string:id_utilisateur>/<string:vo_ni>", methods=["DELETE"])
def delete_voyage_utilisateur(id_utilisateur, vo_ni):
    db = database.Database()
    try:
        db.delete_voyage_user(id_utilisateur, vo_ni)
        response = {
            "status": "success"
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


# Ajoute un voyage à la liste des voyages du client dans la base de données
# INPUT vo_ni: ID du voyage à ajouter
# INPUT id_utilisateur: ID du client auquel on doit ajouter le voyage
# OUTPUT status: Statut de succès de la requête
@app.route("/static/client/add_voyage_utilisateur", methods=["POST"])
def add_voyage_utilisateur():
    db = database.Database()
    data = request.get_json()
    try:
        db.insert_new_voyage_utilisateur(data["vo_ni"], data["id_utilisateur"])
        response = {
            "status": "success"
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


# Recherche tous les voyages ajoutés à la liste du client
# INPUT user_id: ID du client
# OUTPUT voyages: Liste de voyages ajoutés à la liste du client
@app.route("/static/client/get_voyages_utilisateur/<string:user_id>", methods=["GET"])
def get_voyages_utilisateur(user_id):
    db = database.Database()
    try:
        voyages = db.get_voyages_user(user_id)
        return jsonify(voyages)
    except Exception:
        return Response(status=406)


# Ajoute un avis de client à un voyage à la base de données
# INPUT text: Commentaire de l'avis
# INPUT note: Note de l'avis
# INPUT user_id: ID du client
# INPUT vo_ni: ID du voyage lié à l'avis
# OUTPUT status: Statut de succès de la requête
@app.route("/static/client/add-avis", methods=["POST"])
def add_avis():
    db = database.Database()
    data = request.get_json()
    try:
        db.insert_avis(data["text"], data["note"], data["user_id"], data["vo_ni"])
        response = {
            "status": "success"
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


# Retourne tous les avis soumis par le client dans la base de données
# INPUT id_utilisateur: ID du client
# OUTPUT avis: Liste des avis soumis par le client
@app.route("/static/client/get-all-avis/<string:user_id>", methods=["GET"])
def get_all_avis(user_id):
    db = database.Database()
    try:
        avis = db.get_avis(user_id)
        return jsonify(avis)
    except Exception:
        return Response(status=406)


# Supprime un avis du client de la base de données
# INPUT id_utilisateur: ID du client ayant soumis l'avis
# INPUT vo_ni: ID du voyage lié à l'avis
# OUTPUT status: Statut de succès de la requête
@app.route("/static/client/delete-avis/<string:id_utilisateur>/<string:vo_ni>", methods=["DELETE"])
def delete_avis(id_utilisateur, vo_ni):
    db = database.Database()
    try:
        db.supprime_avis(id_utilisateur, vo_ni)
        response = {
            "status": "success"
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


# Modifie un avis du client dans la base de données
# INPUT id_utilisateur: ID du client ayant soumis l'avis
# INPUT vo_ni: ID du voyage lié à l'avis
# OUTPUT status: Statut de succès de la requête
@app.route("/static/client/modify-avis/<string:id_utilisateur>/<string:vo_ni>", methods=["PUT"])
def modify_avis(id_utilisateur, vo_ni):
    db = database.Database()
    data = request.get_json()
    try:
        db.modifier_commentaire(id_utilisateur, vo_ni, data["commentaire"], data["note"])
        response = {
            "status": "success"
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


# Retourne un client selon le nom d'utilisateur et le mot de passe inscrits
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# OUTPUT: Client corresponsant au nom d'utilisateur et au mot de passe inscrits
@app.route("/static/client/get-client", methods=["POST"])
def get_client():
    db = database.Database()
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    clients = db.fetch_client(username)
    if clients == ():
        return Response(status=400)

    for client in clients:
        if bcrypt.check_password_hash(client[2], password):
            response = {
                "status": "success",
                "client": client
            }
            return jsonify(response)
        else:
            return Response(status=400)


# Retourne un conducteur selon le nom d'utilisateur et le mot de passe inscrits
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# OUTPUT: Conducteur corresponsant au nom d'utilisateur et au mot de passe inscrits
@app.route("/static/conducteur/get-conducteur", methods=["POST"])
def get_conducteur():
    db = database.Database()
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    conducteurs = db.fetch_conducteur(username)

    if conducteurs == ():
        return Response(status=400)

    for conducteur in conducteurs:
        if bcrypt.check_password_hash(conducteur[2], password):
            response = {
                "status": "success",
                "conducteur": conducteur
            }
            return jsonify(response)
        else:
            return Response(status=400)


# Retourne un administrateur selon le nom d'utilisateur et le mot de passe inscrits
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# OUTPUT: Administrateur corresponsant au nom d'utilisateur et au mot de passe inscrits
@app.route("/static/admin/get-admin", methods=["POST"])
def get_admin():
    db = database.Database()
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    admins = db.fetch_admin(username)

    if admins == ():
        return Response(status=400)

    for admin in admins:
        if bcrypt.check_password_hash(admin[2], password):
            response = {
                "status": "success",
                "admin": admin
            }
            return jsonify(response)
        else:
            return Response(status=400)

# Crée un nouveau client dans la base de données selon les informations inscrites
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# INPUT last_name: Nom de famille inscrit
# INPUT first_name: Prénom inscrit
# INPUT phone: Numéro de téléphone inscrit
# OUTPUT staus: Statut de succès de la requête
# OUTPUT conducteur: Client nouvellement créé
@app.route("/static/client/create-client", methods=["POST"])
def create_client():
    db = database.Database()
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Vérifie si le nom d'utilisateur est déjà utilisé
    if len(db.fetch_client(data["username"])) > 0:
        db.connection.close()
        return Response(status=500)

    client = db.insert_new_client(data["username"],
                                  hashed_password,
                                  data["last_name"],
                                  data["first_name"],
                                  data["phone"])
    db.connection.close()
    response = {
        "status": "success",
        "client": client
    }
    return jsonify(response)


# Crée un nouveau conducteur dans la base de données
# selon le nom d'utilisateur et le mot de passe inscrits
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# OUTPUT staus: Statut de succès de la requête
# OUTPUT conducteur: Conducteur nouvellement créé
@app.route("/static/conducteur/create-conducteur", methods=["POST"])
def create_conducteur():
    db = database.Database()
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        conducteur = db.insert_new_conducteur(data["username"], hashed_password)

        response = {
            "status": "success",
            "conducteur": conducteur
        }
        return jsonify(response)
    except Exception:
        return Response(status=500)


# Crée un nouvel administrateur dans la base de données
# selon le nom d'utilisateur et le mot de passe inscrits
# INPUT username: Nom d'utilisateur inscrit
# INPUT password: Mot de passe inscrit
# OUTPUT staus: Statut de succès de la requête
# OUTPUT conducteur: Administrateur nouvellement créé
@app.route("/static/admin/create-admin", methods=["POST"])
def create_admin():
    db = database.Database()
    data = request.get_json()
    password = data["password"].encode('utf-8')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if len(db.fetch_admin(data["username"])) > 0:
        db.connection.close()
        return Response(status=500)

    admin = db.insert_new_admin(data["username"], hashed_password)
    db.connection.close()
    response = {
        "status": "success",
        "admin": admin
    }
    return jsonify(response)


# Ajoute un voyage aux spécificités inscrites par l'administrateur à la base de données
# INPUT departure: Ville de départ du voyage
# INPUT destination: Ville de destination du voyage
# INPUT days: Nombre de jours avant le départ du voyage
# INPUT hour: Heure de départ du voyage
# INPUT price: Tarif du voyage pour un client
# OUTPUT staus: Statut de succès de la requête
@app.route("/static/admin/add-voyage", methods=["POST"])
def add_voyage():
    db = database.Database()
    data = request.get_json()
    db.insert_voyage(data["departure"],
                     data["destination"],
                     data["days"],
                     data["hour"],
                     data["price"])
    response = {
        "status": "success",
    }
    return jsonify(response)


# Retourne l'horaire du conducteur spécifié à la date spécifiée
# INPUT id_conducteur: ID du conducteur dont on recherche l'horaire
# INPUT date: Date de l'horaire voulu
# OUTPUT status: Statut de succès de la requête
# OUTPUT horaire: Horaire du conducteur spécifié à la date spécifiée
@app.route("/static/conducteur/get-horaire", methods=["POST"])
def get_horaire_conducteur():
    db = database.Database()
    data = request.get_json()
    horaire = db.fetch_horaire_conducteur(data["id_conducteur"],
                                          data["date"])

    if len(horaire) == 0:
        return Response(status=304)

    response = {
        "status": "success",
        "horaire": horaire[0]
    }
    return jsonify(response)


# Tente d'accorder un congé à un conducteur spécifié à la date spécifiée
# INPUT id_conducteur: ID du conducteur qui veut prendre congé
# INPUT date: Date de la journée de congé voulue
# OUTPUT status: Statut de succès de la requête
@app.route("/static/conducteur/post-day-off-horaire", methods=["POST"])
def post_day_off_request():
    data = request.get_json()
    try:
        db = database.Database()
        db.insert_day_off(data["id_conducteur"], data["date"])
        db.connection.close()
        response = {
            "status": "success",
        }
        return jsonify(response)
    except ValueError:
        return Response(status=304)
    except TypeError:
        return Response(status=400)
    except Exception:
        return Response(status=406)


# Retourne les voyages effectués par le conducteur spécifié à la date spécifiée
# INPUT id_conducteur: ID du conducteur dont on recherche les voyages
# INPUT date: Date des voyages voulus
# OUTPUT status: Statut de succès de la requête
# OUTPUT voyages: Voyages du conducteur spécifié à la date spécifiée
@app.route("/static/conducteur/get-voyages/<string:id_conducteur>/<string:date>", methods=["GET"])
def get_voyages_conduct(id_conducteur, date):
    try:
        db = database.Database()
        voyages = db.get_voyages_conducteur(id_conducteur, date)
        response = {
            "status": "success",
            "voyages": voyages
        }
        return jsonify(response)
    except Exception:
        return Response(status=406)


if __name__ == '__main__':
    app.run()
