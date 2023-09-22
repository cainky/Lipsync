import os
from services.wav2lip_inference import run_wav2lip_inference
from utils import get_uploads_dir

DEFAULT_AUDIO_FILENAME = "audio.webm"
DEFAULT_VIDEO_FILENAME = "face.webm"
DEFAULT_OUTPUT_FILENAME = "output.mp4"


def merge_audio_video(audio_file, video_file):
    uploads_dir = get_uploads_dir()
    audio_path = os.path.join(uploads_dir, DEFAULT_AUDIO_FILENAME)
    video_path = os.path.join(uploads_dir, DEFAULT_VIDEO_FILENAME)
    output_path = os.path.join(uploads_dir, DEFAULT_OUTPUT_FILENAME)

    audio_file.save(audio_path)
    video_file.save(video_path)

    try:
        run_wav2lip_inference(
            face_path=video_path, audio_path=audio_path, outfile_path=output_path
        )
    except Exception:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)
        raise

    return output_path
