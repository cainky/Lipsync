from flask import current_app


def get_uploads_dir():
    return current_app.config["UPLOADS_DIR"]
