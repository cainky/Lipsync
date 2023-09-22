import subprocess
import os

CHECKPOINT_PATH = "wav2lip-hq/checkpoints/wav2lip_gan.pth"
SEGMENTATION_PATH = "wav2lip-hq/checkpoints/face_segmentation.pth"
SR_PATH = "wav2lip-hq/checkpoints/esrgan_max.pth"


def convert_webm_to_wav(input_path, output_path):
    cmd = ["ffmpeg", "-y", "-i", input_path, output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"FFmpeg conversion failed. Error: {result.stderr}")


def convert_to_wav(audio_path):
    """
    Ensure that the provided audio file is in .wav format.
    If it's in .webm, it will be converted to .wav.
    """
    if audio_path.endswith(".webm"):
        output_path = audio_path.replace(".webm", ".wav")
        convert_webm_to_wav(audio_path, output_path)
        # os.remove(audio_path)
        return output_path
    return audio_path


def run_wav2lip_inference(face, audio, outfile):
    audio = convert_to_wav(audio)

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

    result = subprocess.run(cmd, text=True)

    if not os.path.exists(outfile):
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Output video not found after processing. Error: {error_msg}")
    if result.returncode != 0:
        error_msg = result.stderr if result.stderr else result.stdout
        raise Exception(f"Wav2Lip processing failed. Error: {error_msg}")

    return outfile
