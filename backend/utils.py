import os, sys


def get_base_dir(config):
    return config["BASE_DIR"]


def get_uploads_dir(config):
    return get_full_path(get_base_dir(config), "uploads")


def get_wav2lip_dir(config):
    return get_full_path(get_base_dir(config), "wav2lip-hq")


def get_checkpoints_dir(config):
    return get_full_path(get_wav2lip_dir(config), "checkpoints")


def get_wav2lip_env_dir(config):
    return get_full_path(get_wav2lip_dir(config), "wav2lipenv")


def get_full_path(directory, filename):
    fullpath = os.path.normpath(os.path.join(directory, filename))
    return fullpath


def get_python_executable(wav2lip_env_dir):
    if sys.platform.startswith("win"):
        python_path = get_full_path(wav2lip_env_dir, "Scripts")
    else:
        python_path = get_full_path(wav2lip_env_dir, "bin")
    return get_full_path(python_path, "python")
