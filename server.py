from flask import Flask, render_template, request, jsonify, Response

from database import (insert_avis, get_avis, supprime_avis, modifier_commentaire, fetch_client, insert_new_client,
                      get_all_ville, get_voyage, insert_new_voyage_utilisateur, insert_voyage, insert_new_admin,
                      fetch_admin, get_voyages_user, delete_voyage_user, fetch_conducteur, insert_new_conducteur,
                      fetch_horaire_conducteur, insert_day_off, prise_de_conge, get_voyages_conducteur)

from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_cities", methods=["GET"])
@app.route("/static/client/get_cities", methods=["GET"])
@app.route("/static/admin/get_cities", methods=["GET"])
def get_cities():
    try:
        city_names = get_all_ville()
        return jsonify(city_names)
    except Exception as e:
        print(e)
        return Response(status=406)


@app.route("/static/client/get_voyages", methods=["POST"])
def get_voyages():
    try:
        data = request.get_json()
        voyages = get_voyage(data["depart"], data["destination"], data["date_temps"], data["prix"])
        return jsonify(voyages)
    except Exception as e:
        print(e)
        return Response(status=406)


@app.route("/static/client/delete-voyage/<string:id_utilisateur>/<string:vo_ni>", methods=["DELETE"])
def delete_voyage_utilisateur(id_utilisateur, vo_ni):
    delete_voyage_user(id_utilisateur, vo_ni)
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/client/add_voyage_utilisateur", methods=["POST"])
def add_voyage_utilisateur():
    data = request.get_json()
    insert_new_voyage_utilisateur(data["vo_ni"], data["id_utilisateur"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/client/get_voyages_utilisateur/<string:user_id>", methods=["GET"])
def get_voyages_utilisateur(user_id):
    voyages = get_voyages_user(user_id)
    return jsonify(voyages)


@app.route("/static/client/add-avis", methods=["POST"])
def add_avis():
    data = request.get_json()
    insert_avis(data["text"], data["note"], data["user_id"], data["vo_ni"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/client/get-all-avis/<string:user_id>", methods=["GET"])
def get_all_avis(user_id):
    avis = get_avis(user_id)
    return jsonify(avis)


@app.route("/static/client/delete-avis/<string:id_utilisateur>/<string:vo_ni>", methods=["DELETE"])
def delete_avis(id_utilisateur, vo_ni):
    supprime_avis(id_utilisateur, vo_ni)
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/client/modify-avis/<string:id_utilisateur>/<string:vo_ni>", methods=["PUT"])
def modify_avis(id_utilisateur, vo_ni):
    data = request.get_json()
    modifier_commentaire(id_utilisateur, vo_ni, data["commentaire"], data["note"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/client/get-client", methods=["POST"])
def get_client():
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    clients = fetch_client(username)
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


@app.route("/static/conducteur/get-conducteur", methods=["POST"])
def get_conducteur():
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    conducteurs = fetch_conducteur(username)

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


@app.route("/static/admin/get-admin", methods=["POST"])
def get_admin():
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    admins = fetch_admin(username)

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


@app.route("/static/client/create-client", methods=["POST"])
def create_client():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if len(fetch_client(data["username"])) > 0:
        return Response(status=500)

    client = insert_new_client(data["username"],
                               hashed_password,
                               data["last_name"],
                               data["first_name"],
                               data["phone"])
    response = {
        "status": "success",
        "client": client
    }
    return jsonify(response)


@app.route("/static/conducteur/create-conducteur", methods=["POST"])
def create_conducteur():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        conducteur = insert_new_conducteur(data["username"], hashed_password)

        response = {
            "status": "success",
            "conducteur": conducteur
        }
        return jsonify(response)
    except Exception:
        return Response(status=500)


@app.route("/static/admin/create-admin", methods=["POST"])
def create_admin():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if len(fetch_admin(data["username"])) > 0:
        return Response(status=500)

    admin = insert_new_admin(data["username"], hashed_password)

    response = {
        "status": "success",
        "admin": admin
    }
    return jsonify(response)


@app.route("/static/admin/add-voyage", methods=["POST"])
def add_voyage():
    data = request.get_json()
    insert_voyage(data["departure"],
                  data["destination"],
                  data["days"],
                  data["hour"],
                  data["price"])
    response = {
        "status": "success",
    }
    return jsonify(response)


@app.route("/static/conducteur/get-horaire", methods=["POST"])
def get_horaire_conducteur():
    data = request.get_json()
    horaire = fetch_horaire_conducteur(data["id_conducteur"],
                                       data["date"])

    if len(horaire) == 0:
        return Response(status=304)

    response = {
        "status": "success",
        "horaire": horaire[0]
    }
    return jsonify(response)


@app.route("/static/conducteur/post-day-off-horaire", methods=["POST"])
def post_day_off_request():
    data = request.get_json()
    try:
        insert_day_off(data["id_conducteur"], data["date"])
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


@app.route("/static/conducteur/get-voyages/<string:id_conducteur>/<string:date>", methods=["GET"])
def get_voyages_conduct(id_conducteur, date):
    try:
        print(id_conducteur, date)
        voyages = get_voyages_conducteur(id_conducteur, date)
        response = {
            "status": "success",
            "voyages": voyages
        }
        return jsonify(response)
    except:
        return Response(status=406)


if __name__ == '__main__':
    app.run()
