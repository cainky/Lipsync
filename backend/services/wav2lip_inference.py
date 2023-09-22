import subprocess
import os

CHECKPOINT_PATH = "wav2lip-hq/checkpoints/wav2lip_gan.pth"
SEGMENTATION_PATH = "wav2lip-hq/checkpoints/face_segmentation.pth"
SR_PATH = "wav2lip-hq/checkpoints/esrgan_max.pth"


def run_command(cmd):
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        raise Exception(
            f"Command {cmd[0]} failed with return code {result.returncode}."
        )
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


def run_wav2lip_inference(face, audio, outfile):
    audio = convert_to_wav(audio)
    face = convert_to_mp4(face)

    # DEBUG
    print("Starting Wav2Lip inference...")
    print(f"Face file: {face}")
    print(f"Audio file: {audio}")
    print(f"Expected output file: {outfile}")

    cmd = [
        "python",
        "wav2lip-hq/inference.py",
        "--face",
        face,
        "--audio",
        audio,
        "--outfile",
        outfile,
        "--checkpoint_path",
        CHECKPOINT_PATH,
        "--segmentation_path",
        SEGMENTATION_PATH,
        "--sr_path",
        SR_PATH,
    ]

    result = run_command(cmd)

    if not os.path.exists(outfile):
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Output video not found after processing. Error: {error_msg}")

    return outfile
