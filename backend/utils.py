import os
from flask import current_app


def get_base_dir():
    return current_app.config["BASE_DIR"]


def get_uploads_dir():
    return os.path.join(get_base_dir(), "uploads")


def get_wav2lip_dir():
    return os.path.join(get_base_dir(), "wav2lip-hq")


def get_checkpoints_dir():
    return os.path.join(get_wav2lip_dir(), "checkpoints")


def get_wav2lip_env_dir():
    return os.path.join(get_wav2lip_dir(), "wav2lipenv")


def get_full_path(directory, filename):
    fullpath = os.path.normpath(os.path.join(directory, filename))
    return fullpath
