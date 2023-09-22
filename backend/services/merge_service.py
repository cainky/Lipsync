import os
from services.wav2lip_inference import run_wav2lip_inference

DEFAULT_AUDIO_PATH = "audio.webm"
DEFAULT_VIDEO_PATH = "video.webm"
DEFAULT_OUTPUT_PATH = "output.mp4"


def merge_audio_video(audio_file, video_file, upload_folder):
    audio_path = os.path.join(upload_folder, DEFAULT_AUDIO_PATH)
    video_path = os.path.join(upload_folder, DEFAULT_VIDEO_PATH)
    output_path = os.path.join(upload_folder, DEFAULT_OUTPUT_PATH)

    audio_file.save(audio_path)
    video_file.save(video_path)

    try:
        run_wav2lip_inference(
            face_path=video_path, audio_path=audio_path, outfile_path=output_path
        )
    except Exception:
        # Cleanup in case of failure
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)
        raise

    return output_path
