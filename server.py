from flask import Flask, render_template, request, jsonify

from database import insert_avis, get_avis, supprime_avis, modifierCommentaire

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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


if __name__ == '__main__':
    app.run()
