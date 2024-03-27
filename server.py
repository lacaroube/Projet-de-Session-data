from flask import Flask, render_template, request, jsonify

from database import insert_avis

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


if __name__ == '__main__':
    app.run()
