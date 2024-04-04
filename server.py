from flask import Flask, render_template, request, jsonify

from database import (insert_avis, get_avis, supprime_avis, modifier_commentaire, fetch_client, insert_new_client,
                      get_all_ville, get_voyage, insert_new_voyage_utilisateur, insert_voyage, insert_new_admin,
                      fetch_admin, get_voyages_user, delete_voyage_user)

from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_cities", methods=["GET"])
@app.route("/static/get_cities", methods=["GET"])
def get_cities():
    city_names = get_all_ville()
    return jsonify(city_names)


@app.route("/static/get_voyages", methods=["POST"])
def get_voyages():
    data = request.get_json()
    voyages = get_voyage(data["depart"], data["destination"], data["date_temps"], data["prix"])
    return jsonify(voyages)


@app.route("/static/delete-voyage/<string:id_utilisateur>/<string:vo_ni>", methods=["DELETE"])
def delete_voyage_utilisateur(id_utilisateur, vo_ni):
    delete_voyage_user(id_utilisateur, vo_ni)
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/add_voyage_utilisateur", methods=["POST"])
def add_voyage_utilisateur():
    data = request.get_json()
    insert_new_voyage_utilisateur(data["vo_ni"], data["id_utilisateur"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/get_voyages_utilisateur/<string:user_id>", methods=["GET"])
def get_voyages_utilisateur(user_id):
    voyages = get_voyages_user(user_id)
    return jsonify(voyages)


@app.route("/static/add-avis", methods=["POST"])
def add_avis():
    data = request.get_json()
    insert_avis(data["text"], data["note"], data["user_id"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/get-avis/<string:user_id>", methods=["GET"])
def get_all_avis(user_id):
    avis = get_avis(user_id)
    return jsonify(avis)


@app.route("/static/delete-avis/<int:no_avis>", methods=["DELETE"])
def delete_avis(no_avis):
    supprime_avis(no_avis)
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/modify-avis/<int:no_avis>", methods=["PUT"])
def modify_avis(no_avis):
    data = request.get_json()
    modifier_commentaire(no_avis, data["commentaire"], data["note"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/get-client", methods=["POST"])
def get_client():
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    clients = fetch_client(username)

    for client in clients:
        if bcrypt.check_password_hash(client[2], password):
            response = {
                "status": "success",
                "client": client
            }
            return jsonify(response)

    response = {
        "status": "failure",
        "client": []
    }
    return jsonify(response)


@app.route("/static/get-admin", methods=["POST"])
def get_admin():
    data = request.get_json()
    username = data["username"]
    password = data["password"].encode('utf-8')

    admins = fetch_admin(username)

    for admin in admins:
        if bcrypt.check_password_hash(admin[2], password):
            response = {
                "status": "success",
                "admin": admin
            }
            return jsonify(response)

    response = {
        "status": "failure",
        "admin": []
    }
    return jsonify(response)


@app.route("/static/create-client", methods=["POST"])
def create_client():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

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


@app.route("/static/create-admin", methods=["POST"])
def create_admin():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    admin = insert_new_admin(data["username"], hashed_password)
    response = {
        "status": "success",
        "admin": admin
    }
    return jsonify(response)


@app.route("/static/add-voyage", methods=["POST"])
def add_voyage():
    data = request.get_json()
    insert_voyage(data["departure"],
                  data["destination"],
                  data["date_time"],
                  data["price"])
    response = {
        "status": "success",
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
