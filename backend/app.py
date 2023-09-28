from __init__ import create_app
from flask import jsonify

app = create_app(config="production")


@app.route("/")
def index():
    return jsonify(message="Lipsync Backend API")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
