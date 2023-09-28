import os, subprocess
from flask import current_app
from utils import (
    get_checkpoints_dir,
    get_full_path,
    get_wav2lip_env_dir,
    get_python_executable,
)


def run_command(cmd, workdir=None):
    result = subprocess.run(
        cmd, text=True, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        error_details = (
            f"Command '{' '.join(cmd)}' failed with return code {result.returncode}. "
        )
        error_details += f"STDOUT: {result.stdout} "
        error_details += f"STDERR: {result.stderr}"
        raise Exception(error_details)
    return result


def convert_webm_to_wav(input_path, output_path):
    cmd = ["ffmpeg", "-y", "-i", input_path, output_path]
    run_command(cmd)


def convert_to_wav(audio_path):
    if audio_path.endswith(".webm"):
        output_path = audio_path.replace(".webm", ".wav")
        convert_webm_to_wav(audio_path, output_path)
        if os.path.exists(output_path):
            os.remove(audio_path)
            return output_path
        raise Exception(f"Failed to convert {audio_path} to .wav")
    return audio_path


def convert_to_mp4(face_path):
    if face_path.endswith(".webm"):
        output_path = face_path.rsplit(".", 1)[0] + ".mp4"
        cmd = ["ffmpeg", "-y", "-i", face_path, output_path]
        run_command(cmd)
        if os.path.exists(output_path):
            os.remove(face_path)
            return output_path
        raise Exception(f"Failed to convert {face_path} to .mp4")
    return face_path


def run_wav2lip_inference(face_path, audio_path, outfile_path):
    checkpoint_dir = get_checkpoints_dir(current_app.config)
    CHECKPOINT_PATH = get_full_path(checkpoint_dir, "wav2lip_gan.pth")
    SEGMENTATION_PATH = get_full_path(checkpoint_dir, "face_segmentation.pth")
    SR_PATH = get_full_path(checkpoint_dir, "esrgan_max.pth")

    wav2lip_env_dir = get_wav2lip_env_dir(current_app.config)
    python_executable = get_python_executable(wav2lip_env_dir)

    audio_path = convert_to_wav(audio_path)
    face_path = convert_to_mp4(face_path)
    cmd = [
        python_executable,
        "inference.py",
        "--face",
        face_path,
        "--audio",
        audio_path,
        "--outfile",
        outfile_path,
        "--checkpoint_path",
        CHECKPOINT_PATH,
        "--segmentation_path",
        SEGMENTATION_PATH,
        "--sr_path",
        SR_PATH,
    ]

    result = run_command(cmd, workdir="wav2lip-hq")
    if not os.path.exists(outfile_path):
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Error: {error_msg}")

    return outfile_path
