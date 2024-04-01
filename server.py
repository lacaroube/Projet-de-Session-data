from flask import Flask, render_template, request, jsonify

from database import insert_avis, get_avis, supprime_avis, modifierCommentaire, fetch_client, insert_new_client, \
    get_all_ville, get_voyage, insert_new_voyage_utilisateur

from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_cities", methods=["GET"])
def get_cities():
    city_names = get_all_ville()
    return jsonify(city_names)


@app.route("/get_voyages", methods=["POST"])
def get_voyages():
    data = request.get_json()
    voyages = get_voyage(data["depart"], data["destination"], data["date_temps"], data["prix"])
    return jsonify(voyages)


@app.route("/add_voyage_utilisateur", methods=["POST"])
def add_voyage_utilisateur():
    data = request.get_json()
    insert_new_voyage_utilisateur(data["vo_ni"], data["id_utilisateur"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/add-avis", methods=["POST"])
def add_avis():
    data = request.get_json()
    insert_avis(data["text"], data["note"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/get-avis", methods=["GET"])
def get_all_avis():
    avis = get_avis()
    return jsonify(avis)


@app.route("/delete-avis/<int:no_avis>", methods=["DELETE"])
def delete_avis(no_avis):
    supprime_avis(no_avis)
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/modify-avis/<int:no_avis>", methods=["PUT"])
def modify_avis(no_avis):
    data = request.get_json()
    modifierCommentaire(no_avis, data["commentaire"], data["note"])
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
                "clients": clients
            }
            return jsonify(response)

    response = {
        "status": "failure",
        "clients": []
    }
    return jsonify(response)


@app.route("/static/create-client", methods=["POST"])
def create_client():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    insert_new_client(data["id"],
                      data["username"],
                      hashed_password,
                      data["last_name"],
                      data["first_name"],
                      data["birth_date"],
                      data["phone"],
                      data["address"])
    response = {
        "status": "success"
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
