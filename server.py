from flask import Flask, render_template, request, jsonify

from database import insert_avis, get_avis, supprime_avis, modifier_commentaire

from flask_bcrypt import Bcrypt

from database import insert_avis, fetch_client, insert_new_client

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/add-avis", methods=["POST"])
def add_avis():
    data = request.get_json()
    insert_avis(data["text"], data["note"], data["user_id"])
    response = {
        "status": "success"
    }
    return jsonify(response)


@app.route("/static/get-avis/<int:user_id>", methods=["GET"])
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


@app.route("/static/create-client", methods=["POST"])
def create_client():
    data = request.get_json()
    password = data["password"].encode('utf-8')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    client = insert_new_client(data["id"],
                               data["username"],
                               hashed_password,
                               data["last_name"],
                               data["first_name"],
                               data["birth_date"],
                               data["phone"],
                               data["address"])
    response = {
        "status": "success",
        "client": client
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
