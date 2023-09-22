import os, subprocess

CHECKPOINT_PATH = "wav2lip-hq/checkpoints/wav2lip_gan.pth"
SEGMENTATION_PATH = "wav2lip-hq/checkpoints/face_segmentation.pth"
SR_PATH = "wav2lip-hq/checkpoints/esrgan_max.pth"

DEFAULT_AUDIO_PATH = "audio.webm"
DEFAULT_VIDEO_PATH = "video.webm"
DEFAULT_OUTPUT_PATH = "output.mp4"


def run_wav2lip_inference(face, audio, outfile):
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

    result = subprocess.run(cmd, capture_output=True, text=True)

    if not os.path.exists(outfile):
        raise Exception("Output video not found after processing.")
    if result.returncode != 0:
        raise Exception(f"Wav2Lip processing failed. Error: {result.stderr}")

    return outfile


def merge_audio_video(audio_file, video_file, upload_folder):
    audio_path = os.path.join(upload_folder, DEFAULT_AUDIO_PATH)
    video_path = os.path.join(upload_folder, DEFAULT_VIDEO_PATH)
    output_path = os.path.join(upload_folder, DEFAULT_OUTPUT_PATH)

    audio_file.save(audio_path)
    video_file.save(video_path)

    run_wav2lip_inference(face=video_path, audio=audio_path, outfile=output_path)

    return output_path
