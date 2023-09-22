import os
from flask import Flask, jsonify
from flask_cors import CORS
import routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

routes.init_app(app)


@app.route("/")
def index():
    return jsonify(message="Lipsync Backend API")


if __name__ == "__main__":
    app.run(debug=True)
